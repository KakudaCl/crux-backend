"""
Try Record Model
トライ記録テーブルのモデル定義
"""

from sqlalchemy import Column, BigInteger, Integer, Date, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.database import Base


class TryRecord(Base):
    """トライ記録モデル"""

    __tablename__ = "try_record"

    # カラム定義
    try_id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="トライID"
    )
    gym_id = Column(
        Integer,
        ForeignKey("gym_info.gym_id", ondelete="CASCADE"),
        nullable=False,
        comment="ジムID",
    )
    problem_number = Column(Integer, nullable=True, default=None, comment="課題番号")
    area_id = Column(
        Integer,
        ForeignKey("area_info.area_id", ondelete="CASCADE"),
        nullable=True,
        default=None,
        comment="エリアID",
    )
    grade_id = Column(
        Integer,
        ForeignKey("grade_info.grade_id", ondelete="CASCADE"),
        nullable=False,
        comment="グレードID",
    )
    result_id = Column(
        Integer,
        ForeignKey("result_info.result_id", ondelete="CASCADE"),
        nullable=False,
        comment="トライ結果ID",
    )
    try_date = Column(Date, nullable=True, default=None, comment="トライ日")
    day_count = Column(Integer, nullable=True, default=None, comment="トライ日数")
    remarks = Column(String(30), nullable=True, default=None, comment="備考")
    is_deleted = Column(Integer, nullable=False, default=0, comment="削除フラグ")
    created_at = Column(TIMESTAMP, nullable=False, comment="作成日時")
    updated_at = Column(TIMESTAMP, nullable=False, comment="更新日時")
    deleted_at = Column(TIMESTAMP, nullable=True, default=None, comment="削除日時")

    # リレーションシップ
    gym = relationship("GymInfo", back_populates="try_records")
    grade = relationship("GradeInfo", back_populates="try_records")
    area = relationship("AreaInfo", back_populates="try_records")
    result = relationship("ResultInfo", back_populates="try_records")

    def __repr__(self) -> str:
        return (
            f"<TryRecord(id={self.try_id}, gym_id={self.gym_id}, "
            f"grade_id={self.grade_id}, problem={self.problem_number}, "
            f"result_id={self.result_id}, date={self.try_date})>"
        )
