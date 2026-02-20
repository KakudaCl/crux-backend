"""
Database Configuration
SQLAlchemyを使用したデータベース接続の設定と管理
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# データベースエンジンの作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # DEBUGモードの時はSQLをログ出力
    pool_pre_ping=True,  # 接続の有効性を事前にチェック
    pool_size=5,  # コネクションプールのサイズ
    max_overflow=10,  # プールサイズを超えた場合の最大接続数
)

# セッションファクトリーの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルの基底クラス
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションを取得する依存性注入用関数

    FastAPIのDependency Injectionで使用される
    各リクエストごとに新しいセッションを作成し、処理終了後にクローズする

    Yields:
        Session: SQLAlchemyのデータベースセッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    データベースの初期化
    全てのテーブルを作成する（本番環境ではAlembicを使用することを推奨）
    """
    Base.metadata.create_all(bind=engine)
