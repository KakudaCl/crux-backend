"""
Area Info Model
エリア情報テーブルのモデル定義
"""

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class AreaInfo(Base):
    """エリア情報モデル"""
    
    __tablename__ = "area_info"
    
    # カラム定義
    area_id = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=True,
        comment="エリアID"
    )
    area_name = Column(
        String(10),
        nullable=False,
        unique=True,
        comment="エリア名"
    )
    
    # リレーションシップ
    try_records = relationship(
        "TryRecord",
        back_populates="area",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<AreaInfo(id={self.area_id}, name='{self.area_name}')>"
