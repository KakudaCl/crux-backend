"""
Try Record Model
トライ記録テーブルのモデル定義
"""

from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class TryRecord(Base):
    """トライ記録モデル"""
    
    __tablename__ = "try_record"
    
    # カラム定義
    try_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="トライID"
    )
    gym_id = Column(
        BigInteger,
        ForeignKey("gym_info.gym_id", ondelete="CASCADE"),
        nullable=False,
        comment="ジムID"
    )
    grade_id = Column(
        BigInteger,
        ForeignKey("grade_info.grade_id", ondelete="CASCADE"),
        nullable=False,
        comment="グレードID"
    )
    problem_number = Column(
        Integer,
        nullable=False,
        comment="課題番号"
    )
    area_id = Column(
        BigInteger,
        ForeignKey("area_info.area_id", ondelete="SET NULL"),
        nullable=True,
        comment="エリアID"
    )
    result_id = Column(
        BigInteger,
        ForeignKey("result_info.result_id", ondelete="CASCADE"),
        nullable=False,
        comment="トライ結果ID"
    )
    try_date = Column(
        DateTime,
        nullable=False,
        comment="トライ日"
    )
    day_count = Column(
        Integer,
        nullable=True,
        comment="トライ日数"
    )
    
    # リレーションシップ
    gym = relationship(
        "GymInfo",
        back_populates="try_records"
    )
    grade = relationship(
        "GradeInfo",
        back_populates="try_records"
    )
    area = relationship(
        "AreaInfo",
        back_populates="try_records"
    )
    result = relationship(
        "ResultInfo",
        back_populates="try_records"
    )
    
    def __repr__(self) -> str:
        return (
            f"<TryRecord(id={self.try_id}, gym_id={self.gym_id}, "
            f"grade_id={self.grade_id}, problem={self.problem_number}, "
            f"result_id={self.result_id}, date={self.try_date})>"
        )
