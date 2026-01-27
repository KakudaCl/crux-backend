from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベース接続URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://crux_user:crux_password@localhost:5432/crux_db"
)

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)

# セッションローカルの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()


def get_db():
    """
    データベースセッションの依存性注入用関数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
