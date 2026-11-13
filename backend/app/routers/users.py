from fastapi import (
    Response, 
    Cookie, 
    File, 
    UploadFile, 
    APIRouter, 
    Depends, 
    Query, 
    Path, 
    HTTPException 
)
from core.database.schema.users import UserCreate, ProfileUpdate
from core.database.models.users import User
from core.database.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from core.security import *
from logger import logger
import shutil
import uuid
import os

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/signup")
def create_user(validate: UserCreate, img: UploadFile = File(...), db: Session = Depends(get_db)):
    
    try:
        user = db.query(User).filter(User.phone_number == validate.user_phone_number).first()
        if user:
            raise HTTPException(status_code = 409, detail = "Bad Request, Phone Number Has Used Before.")
            
        file_path = os.path.splitext(img.filename)[1]
        unique_name = f"{uuid.uuid4()}{file_path}"
        file_url = f"/uploads/{unique_name}"
        file_location = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_location, "wb") as b:
            shutil.copyfileobj(img.file, b)

        new_user = User(
            name = validate.user_name,
            phone_number = validate.user_phone_number,
            description = validate.user_description,
            photo_url = file_url
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "status": "201, created"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        os.remove(file_location)
        logger.error(f"Error in create_user: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.post("/login")
def login_user(user_name: str, phone_number: int, db: Session = Depends(get_db), response: Response):

    try:
        user = db.query(User).filter(User.phone_number == phone_number, User.name == user_name).first()
        if user:
            token = create_hashed_token()
            user.token = token
            response.set_cookie (
                key = "user_token",
                value = token,
                httponly = True,
                secure = False,
                samesite = "lax"
            )
            return { 
                "status": "200"
            }
        else:
            raise HTTPException(status_code = 404, detail = "Signup First.")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in login_user: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.get("/{user_name}")
def get_user(user_name: str = Path(...), phone_number: Annotated[int, Query(...)], db: Session = Depends(get_db)):

    try:
        user = db.query(User).filter(User.phone_number == phone_number, User.name == user_name).first()
        if user:
            return {
                "status": "200",
                "user_name": user.name,
                "user_description": user.description,
                "user_img": user.photo_url,
                "user_posts": list(user.posts)
            }
        else:
            raise HTTPException(status_code=404, detail=f"User {user_name} not found.")

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in get_user: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.put("/profile_update")
def update_profile(update_validate: ProfileUpdatecookie: str | None = Cookie(default=None), db: Session = Depends(get_db)):

    try:
        if not cookie:
            raise HTTPException(status_code = 400, detail = "Havn't access, Didn't Signup")
        else:
            user = db.query(User).filter(User.token == cookie).first()
            if user:
                user.name = update_validate.user_name
                user.description = update_validate.user_description
                db.commit()
                db.refresh(user)
            else:
                raise HTTPException(status_code=401, detail=f"Invalid token, please login again.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error in update_profile: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")


@router.delete("/delete")
def delete_user(cookie: str | None = Cookie(default=None), db: Session = Depends(get_db)):

    try:
        if not cookie:
            raise HTTPException(status_code = 400, detail = "Havn't access, Didn't Signup")
        else:
            user = db.query(User).filter(User.token == cookie).first()
            if user:
                db.delete(user)
                db.commit()
            else:
                raise HTTPException(status_code=401, detail=f"Invalid token.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error in delete_user: {str(e)}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error.")