from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Challenge(Base):
    """
    ボルダリングの挑戦結果を記録するモデル
    """
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False, comment="挑戦者名")
    grade = Column(String(20), nullable=False, comment="課題のグレード（例：6級、5級、V0など）")
    climb_type = Column(String(50), default="ボルダリング", comment="クライミングの種類")
    success = Column(Boolean, default=False, comment="成功したかどうか")
    attempts = Column(Integer, default=1, comment="挑戦回数")
    notes = Column(Text, nullable=True, comment="メモ・コメント")
    gym_name = Column(String(200), nullable=True, comment="ジム名")
    location = Column(String(200), nullable=True, comment="場所")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="記録日時")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新日時")

    def __repr__(self):
        return f"<Challenge(id={self.id}, user_name='{self.user_name}', grade='{self.grade}', success={self.success})>"
