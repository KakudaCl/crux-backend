"""
FastAPI Application Entry Point
CRUX Backend APIのメインアプリケーション
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.database import get_db, engine
from app.routers import trylogs, gyms, grades, areas

# 環境変数の読み込み
APP_NAME = os.getenv("APP_NAME", "CRUX Backend API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# FastAPIアプリケーションの作成
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="ボルダリングのトライ記録を管理するバックエンドAPI",
    debug=DEBUG,
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(gyms.router, prefix="/api", tags=["共通"])
app.include_router(grades.router, prefix="/api", tags=["共通"])
app.include_router(areas.router, prefix="/api", tags=["共通"])
app.include_router(trylogs.router, prefix="/api", tags=["トライログ"])


@app.on_event("startup")
async def startup_event():
    """
    アプリケーション起動時の処理
    データベース接続の確認を行う
    """
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    print("Database connection check...")

    # データベース接続の確認
    try:
        # エンジンの接続テスト
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and configuration is correct.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    アプリケーション終了時の処理
    """
    print(f"Shutting down {APP_NAME}")
    engine.dispose()


@app.get("/")
async def root():
    """
    ルートエンドポイント
    APIの基本情報を返す
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    ヘルスチェックエンドポイント
    アプリケーションとデータベースの状態を確認
    """
    try:
        # データベース接続の確認
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "version": APP_VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=DEBUG)
