from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, auth
from dotenv import load_dotenv

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


@app.get("/")
async def root():
    return {"message": "Welcome to Huhsame AI Chat API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
