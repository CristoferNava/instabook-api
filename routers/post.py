from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_post
from routers.schemas import PostBase, PostDisplay


router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="image_url_type must be 'absolute' or 'relative'")
    return db_post.create_post(db, request)
