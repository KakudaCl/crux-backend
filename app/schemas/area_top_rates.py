"""
Area Top Rates Schemas
エリア別完登率取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class AreaInfo(BaseModel):
    """
    エリア別情報スキーマ
    データがないエリアも含め、全てのエリア名を項目として返す。
    """
    area_name: str = Field(..., description="エリア名（例: 強傾斜）")
    top_rate: Optional[float] = Field(None, description="完登率（%）。データがない場合はnull")
    boulder_count: int = Field(0, description="挑戦課題数")
    top_count: int = Field(0, description="完登数")

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
