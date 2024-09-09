from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.api import chat, auth
from app.db import get_db, SessionLocal  # 데이터베이스 설정 가져오기

load_dotenv()

app = FastAPI(
    title="HuhSame AI Chat API",
    description="AI-powered chat service using LangChain and OpenAI",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 출처를 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 추가
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


# 데이터베이스 연결 테스트
@app.on_event("startup")
def startup_event():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # 간단한 쿼리 실행으로 데이터베이스 연결 테스트
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.get("/")
async def root():
    return {"message": "Welcome to Huhsame AI Chat API"}


# 데이터베이스 연결 상태 확인을 위한 엔드포인트 추가
@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT 1")  # 간단한 쿼리 실행으로 데이터베이스 연결 테스트
        return {"status": "Database connection successful", "result": result.fetchone()}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
