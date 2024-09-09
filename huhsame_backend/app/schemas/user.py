from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import crud, schemas
from app.db import get_db

router = APIRouter()


class RegisterUser(BaseModel):
    email: str
    username: str
    bubble_user_id: str  # 버블의 사용자 고유 ID


@router.post("/register")
async def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    # 이메일이 이미 존재하는지 확인
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        # 이미 등록된 사용자인 경우 업데이트를 고려할 수 있음
        return {"message": "User already exists."}

    # 새로운 사용자 생성
    new_user = schemas.UserCreate(
        email=user.email,
        username=user.username,
        password="",  # 비밀번호는 버블에서 관리되므로 서버에서는 비어 있을 수 있음
        bubble_user_id=user.bubble_user_id,
    )
    created_user = crud.create_user(db=db, user=new_user)
    return {"message": "User registered successfully", "user_id": created_user.id}
