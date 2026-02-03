"""
Top Rates Schemas
完登率取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


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


class HalfYearInfo(BaseModel):
    """
    半期情報スキーマ
    """
    period: str = Field(..., description="期間（上半期/下半期）")
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
    monthly_info: List[MonthlyInfo] = Field(
        ..., description="月別情報（月、上半期、下半期、年間を含む）"
    )

    class Config:
        from_attributes = True


class TopRateResponse(BaseModel):
    """
    完登率取得APIのレスポンススキーマ
    """
    result_info: List[GradeTopRate] = Field(..., description="完登率情報一覧")

    class Config:
        from_attributes = True
