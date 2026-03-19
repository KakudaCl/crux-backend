"""
Areas Schemas
エリア名取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


class AreaNameItem(BaseModel):
    """
    エリア名情報スキーマ
    """

    area_name: str = Field(..., description="エリア名", example="スラブ")
    area_id: int = Field(..., description="エリアID", example=7)

    class Config:
        from_attributes = True


class AreasNameResponse(BaseModel):
    """
    エリア名取得APIのレスポンススキーマ
    """

    areas_info: List[AreaNameItem] = Field(..., description="エリア名一覧")

    class Config:
        from_attributes = True
