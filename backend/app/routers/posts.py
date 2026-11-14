from fastapi import (
    Cookie, 
    File, 
    UploadFile, 
    APIRouter, 
    Depends, 
    Form, 
    HTTPException 
)
from app.core.database.models.users import User
from app.core.database.models.posts import Post
from app.core.database.database import get_db, engine, Base
from sqlalchemy.orm import Session
from app.logger import logger
import shutil
import uuid
import os

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
def create_post(
    post_content: str = Form(...), 
    cookie: str | None = Cookie(default=None), 
    img: UploadFile | None = File(None), 
    db: Session = Depends(get_db)
):
    file_location = None

    try:

        if not cookie:
            raise HTTPException(status_code=401, detail="Unauthorized, please login first.")

        user = db.query(User).filter(User.token == cookie).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        file_url = None
        if img is not None:
            file_path = os.path.splitext(img.filename)[1]
            unique_name = f"{uuid.uuid4()}{file_path}"
            file_url = f"/uploads/{unique_name}"
            file_location = os.path.join(UPLOAD_DIR, unique_name)

            with open(file_location, "wb") as b:
                shutil.copyfileobj(img.file, b)

        new_post = Post(
            content = post_content,
            poster_id = user.id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"status": "201, created"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        if file_location and os.path.exists(file_location):
            os.remove(file_location)
        logger.error(f"Error in create_post: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).all()
        if posts:
            posts_list = []
            for post in posts:
                posts_list.append({
                    "poster_name": post.poster.name if post.poster else "Unknown",
                    "post_content": post.content,
                    "post_date": post.post_date.isoformat() if post.post_date else None
                })
            return {"status": "200", "posts": posts_list}
        else:
            return {"posts": "No Posts Found."}
    except Exception as e:
        db.rollback()
        logger.error(f"Error in get_posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.get("/user")
def get_user_posts(cookie: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    try:
        if not cookie:
            raise HTTPException(status_code=401, detail="Unauthorized, please login first.")

        user = db.query(User).filter(User.token == cookie).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        posts = db.query(Post).filter(Post.poster_id == user.id).all()
        if posts:
            posts_list = []
            for post in posts:
                posts_list.append({
                    "poster_name": user.name,
                    "post_content": post.content,
                    "post_date": post.post_date.isoformat() if post.post_date else None
                })
            return {"status": "200", "posts": posts_list}
        else:
            return {"posts": "No Posts Found."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in get_user_posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.put("/update")
def update_post(
    post_content: str = Form(...),
    cookie: str | None = Cookie(default=None), 
    db: Session = Depends(get_db)
):
    try:
        if not cookie:
            raise HTTPException(status_code=401, detail="Invalid token, login again.")
        
        user = db.query(User).filter(User.token == cookie).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        post = db.query(Post).filter(Post.poster_id == user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found.")

        post.content = post_content
        db.commit()
        db.refresh(post)
        return {"status": "200, updated"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in update_post: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.delete("/delete")
def delete_post(cookie: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    try:
        if not cookie:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        user = db.query(User).filter(User.token == cookie).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        post = db.query(Post).filter(Post.poster_id == user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found.")

        db.delete(post)
        db.commit()
        return {"status": "200, deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in delete_post: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
