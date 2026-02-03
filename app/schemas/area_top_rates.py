"""
Area Top Rates Schemas
エリア別完登率取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


class AreaInfo(BaseModel):
    """
    エリア別情報スキーマ
    """
    area_name: str = Field(..., description="エリア名（例: 強傾斜）")
    top_rate: float = Field(..., description="完登率（%）")
    boulder_count: int = Field(..., description="挑戦課題数")
    top_count: int = Field(..., description="完登数")

    class Config:
        from_attributes = True


class GradeAreaTopRate(BaseModel):
    """
    グレード別エリア完登率情報スキーマ
    """
    grade: str = Field(..., description="グレード名（例: 3級）")
    area_info: List[AreaInfo] = Field(..., description="エリア別情報")

    class Config:
        from_attributes = True


class AreaTopRateResponse(BaseModel):
    """
    エリア別完登率取得APIのレスポンススキーマ
    """
    result_info: List[GradeAreaTopRate] = Field(..., description="完登率情報一覧")

    class Config:
        from_attributes = True
