from fastapi import APIRouter

# APIRouter 객체 생성
router = APIRouter()


# 예시 엔드포인트 정의
@router.post("/login")
async def login():
    return {"message": "User login"}


@router.post("/signup")
async def signup():
    return {"message": "User signup"}


# 필요한 추가 엔드포인트들을 여기에 정의합니다.
