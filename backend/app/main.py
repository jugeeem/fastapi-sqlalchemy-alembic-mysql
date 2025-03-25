from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .middleware import AccessLoggingMiddleware

from app.config import settings
from app.interfaces.api.v1.api import api_router
from app.infrastructure.database import init_db

app = FastAPI(
    title="FastAPI Application",
    description="FastAPIアプリケーションサービス",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ミドルウェアを追加
app.add_middleware(AccessLoggingMiddleware)

# APIルーターの登録
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
