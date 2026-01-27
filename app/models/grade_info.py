"""
Grade Info Model
グレード情報テーブルのモデル定義
"""

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class GradeInfo(Base):
    """グレード情報モデル"""
    
    __tablename__ = "grade_info"
    
    # カラム定義
    grade_id = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=True,
        comment="グレードID"
    )
    grade_name = Column(
        String,
        nullable=False,
        unique=True,
        comment="グレード名"
    )
    grade_color = Column(
        String(6),
        nullable=False,
        comment="グレード色（カラーコード）"
    )
    
    # リレーションシップ
    try_records = relationship(
        "TryRecord",
        back_populates="grade",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<GradeInfo(id={self.grade_id}, name='{self.grade_name}', color='{self.grade_color}')>"
