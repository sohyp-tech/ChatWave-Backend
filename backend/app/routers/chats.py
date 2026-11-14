from fastapi import (
    WebSocket,
    WebSocketDisconnect, 
    APIRouter, 
    Depends, 
    Query, 
    Path,
    Body
)
from app.core.database.models.users import User
from app.core.database.models.chats import Chat, Message
from app.core.database.database import get_db, engine, Base
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.security import *
import datetime

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)

Base.metadata.create_all(bind=engine)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        old = self.active_connections.get(user_id)
        if old:
            await old.close()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
    
    async def send_to_user(self, user_id: int, payload: dict) -> bool:
        ws = self.active_connections.get(user_id)
        if ws is None:
            return False
        await ws.send_json(payload)
        return True

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int = Path(...), db: Session = Depends(get_db)):

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()

            to = data.get("to")
            body = data.get("body")
            if not to or not body:
                await websocket.send_json({"error": "missing 'to' or 'body'"})
                continue
            
            chat = db.query(Chat).filter(
                ((Chat.user1_id == user_id) & (Chat.user2_id == to)) |
                ((Chat.user1_id == to) & (Chat.user2_id == user_id))
            ).first()

            if not chat:
                chat = Chat(user1_id=min(user_id, to), user2_id=max(user_id, to))
                db.add(chat)
                db.commit()
                db.refresh(chat)
            
            msg = Message(chat_id=chat.id, sender_id=user_id, content=body)
            db.add(msg)
            db.commit()
            db.refresh(msg)

            payload = {
                "id": msg.id,
                "chat_id": chat.id,
                "from": user_id,
                "to": to,
                "body": body,
                "at": msg.date.isoformat(),
            }

            await manager.send_to_user(to, payload)

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(user_id)


@router.get("/{user_id}/{other_id}")
def get_chat(user_id: int = Path(...), other_id: int = Path(...), db: Session = Depends(get_db)):

    chat = db.query(Chat).filter(
        ((Chat.user1_id == user_id) & (Chat.user2_id == other_id)) |
        ((Chat.user1_id == other_id) & (Chat.user2_id == user_id))
    ).first()

    if not chat:
        return { "messages": [] }
    
    messages = db.query(Message).filter(Message.chat_id == chat.id).order_by(Message.date).all()
    
    return {
        "messages": [ 
            { 
                "id": m.id, 
                "from": m.sender_id, 
                "body": m.content, 
                "at": m.date, 
                "is_read": m.is_read 
            } for m in messages 
        ]
    }
