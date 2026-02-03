"""
Area Info Model
エリア情報テーブルのモデル定義
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class AreaInfo(Base):
    """エリア情報モデル"""
    
    __tablename__ = "area_info"
    
    # カラム定義
    area_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="エリアID"
    )
    gym_id = Column(
        Integer,
        ForeignKey("gym_info.gym_id", ondelete="CASCADE"),
        nullable=False,
        comment="ジムID"
    )
    area_name = Column(
        String(10),
        nullable=False,
        comment="エリア名"
    )
    
    # リレーションシップ
    gym = relationship(
        "GymInfo",
        back_populates="areas"
    )
    try_records = relationship(
        "TryRecord",
        back_populates="area",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<AreaInfo(id={self.area_id}, name='{self.area_name}')>"
