"""
Prefecture Info Model
都道府県情報テーブルのモデル定義
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class PrefectureInfo(Base):
    """都道府県情報モデル"""
    
    __tablename__ = "prefecture_info"
    
    # カラム定義
    prefecture_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="都道府県ID"
    )
    prefecture_name = Column(
        String(20),
        nullable=False,
        comment="都道府県名"
    )
    
    # リレーションシップ
    gyms = relationship(
        "GymInfo",
        back_populates="prefecture",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<PrefectureInfo(id={self.prefecture_id}, name='{self.prefecture_name}')>"
