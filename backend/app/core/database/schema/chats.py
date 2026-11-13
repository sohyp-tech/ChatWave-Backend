from pydantic import BaseModel

class ChatCreate(BaseModel):
    chat_room: str
    user_sender_id: int
    user_reveirser_id: int
    chat_content: str
    chat_date: str