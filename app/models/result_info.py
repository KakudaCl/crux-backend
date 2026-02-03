"""
Result Info Model
トライ結果情報テーブルのモデル定義
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ResultInfo(Base):
    """トライ結果情報モデル"""
    
    __tablename__ = "result_info"
    
    # カラム定義
    result_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="トライ結果ID"
    )
    result_name = Column(
        String(10),
        nullable=False,
        comment="トライ結果名（FLASH/TOP/ZONE/NOSCORE）"
    )
    
    # リレーションシップ
    try_records = relationship(
        "TryRecord",
        back_populates="result",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<ResultInfo(id={self.result_id}, name='{self.result_name}')>"
