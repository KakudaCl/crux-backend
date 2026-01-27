"""
FastAPI Application Entry Point
CRUX Backend APIのメインアプリケーション
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db, engine
from app.models import Base

# FastAPIアプリケーションの作成
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ボルダリングのトライ記録を管理するバックエンドAPI",
    debug=settings.DEBUG
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    アプリケーション起動時の処理
    データベース接続の確認を行う
    """
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📊 Database URL: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'}")
    
    # データベース接続の確認
    try:
        # エンジンの接続テスト
        with engine.connect() as connection:
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️  Please ensure PostgreSQL is running and configuration is correct.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    アプリケーション終了時の処理
    """
    print(f"👋 Shutting down {settings.APP_NAME}")
    engine.dispose()


@app.get("/")
async def root():
    """
    ルートエンドポイント
    APIの基本情報を返す
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "Welcome to CRUX Backend API"
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
        "version": settings.APP_VERSION
    }


# 将来的なAPIルーターの追加場所
# app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
