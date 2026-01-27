from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChallengeBase(BaseModel):
    """
    挑戦記録の基本スキーマ
    """
    user_name: str = Field(..., min_length=1, max_length=100, description="挑戦者名")
    grade: str = Field(..., min_length=1, max_length=20, description="課題のグレード")
    climb_type: str = Field(default="ボルダリング", max_length=50, description="クライミングの種類")
    success: bool = Field(default=False, description="成功したかどうか")
    attempts: int = Field(default=1, ge=1, description="挑戦回数")
    notes: Optional[str] = Field(None, description="メモ・コメント")
    gym_name: Optional[str] = Field(None, max_length=200, description="ジム名")
    location: Optional[str] = Field(None, max_length=200, description="場所")


class ChallengeCreate(ChallengeBase):
    """
    挑戦記録作成用スキーマ
    """
    pass


class ChallengeUpdate(BaseModel):
    """
    挑戦記録更新用スキーマ（すべてのフィールドをオプショナルに）
    """
    user_name: Optional[str] = Field(None, min_length=1, max_length=100)
    grade: Optional[str] = Field(None, min_length=1, max_length=20)
    climb_type: Optional[str] = Field(None, max_length=50)
    success: Optional[bool] = None
    attempts: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None
    gym_name: Optional[str] = Field(None, max_length=200)
    location: Optional[str] = Field(None, max_length=200)


class ChallengeResponse(ChallengeBase):
    """
    挑戦記録レスポンス用スキーマ
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
