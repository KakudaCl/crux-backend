from pydantic import BaseModel, Field
from typing import Optional, List
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


# ========================================
# 完登率取得API用のスキーマ
# ========================================

class MonthlyInfo(BaseModel):
    """
    月別情報スキーマ
    """
    month: str = Field(..., description="月（例: 1月）")
    top_rate: float = Field(..., description="完登率（%）")
    boulder_count: int = Field(..., description="挑戦課題数")
    top_count: int = Field(..., description="完登数")

    class Config:
        from_attributes = True


class GradeTopRate(BaseModel):
    """
    グレード別完登率情報スキーマ
    """
    grade: str = Field(..., description="グレード名（例: 3級）")
    monthly_info: List[MonthlyInfo] = Field(..., description="月別情報")

    class Config:
        from_attributes = True


class TopRateResponse(BaseModel):
    """
    完登率取得APIのレスポンススキーマ
    """
    result_info: List[GradeTopRate] = Field(..., description="完登率情報一覧")

    class Config:
        from_attributes = True
