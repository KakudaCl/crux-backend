"""
Gym Info Model
ジム情報テーブルのモデル定義
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class GymInfo(Base):
    """ジム情報モデル"""

    __tablename__ = "gym_info"

    # カラム定義
    gym_id = Column(Integer, primary_key=True, autoincrement=True, comment="ジムID")
    gym_name = Column(String(20), nullable=False, comment="ジム名称")
    prefecture_id = Column(
        Integer,
        ForeignKey("prefecture_info.prefecture_id", ondelete="CASCADE"),
        nullable=False,
        comment="都道府県ID",
    )

    # リレーションシップ
    prefecture = relationship("PrefectureInfo", back_populates="gyms")
    grades = relationship(
        "GradeInfo", back_populates="gym", cascade="all, delete-orphan"
    )
    areas = relationship("AreaInfo", back_populates="gym", cascade="all, delete-orphan")
    try_records = relationship(
        "TryRecord", back_populates="gym", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<GymInfo(id={self.gym_id}, name='{self.gym_name}', prefecture_id={self.prefecture_id})>"
