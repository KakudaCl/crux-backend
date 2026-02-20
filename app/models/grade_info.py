"""
Grade Info Model
グレード情報テーブルのモデル定義
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class GradeInfo(Base):
    """グレード情報モデル"""

    __tablename__ = "grade_info"

    # カラム定義
    grade_id = Column(
        Integer, primary_key=True, autoincrement=True, comment="グレードID"
    )
    gym_id = Column(
        Integer,
        ForeignKey("gym_info.gym_id", ondelete="CASCADE"),
        nullable=False,
        comment="ジムID",
    )
    grade_name = Column(String(10), nullable=False, comment="グレード名")
    grade_color = Column(
        String(6), nullable=False, comment="グレード色（カラーコード）"
    )

    # リレーションシップ
    gym = relationship("GymInfo", back_populates="grades")
    try_records = relationship(
        "TryRecord", back_populates="grade", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<GradeInfo(id={self.grade_id}, name='{self.grade_name}', color='{self.grade_color}')>"
