from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm.session import Session
from typing import List
import string
import random
import shutil
from db.database import get_db
from db import db_post
from routers.schemas import PostBase, PostDisplay, UserAuth
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create_post(request: PostBase,
                db: Session = Depends(get_db),
                current_user: UserAuth = Depends(get_current_user)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="image_url_type must be 'absolute' or 'relative'")
    return db_post.create_post(db, request)


@router.get("/all", response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post("/image")
def upload_image(image: UploadFile = File(...),
                 current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(5))
    filename = f"_{rand_str}.".join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}


@router.delete("/delete/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(db, id, current_user.id)
