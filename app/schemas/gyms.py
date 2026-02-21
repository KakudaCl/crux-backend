"""
Gyms Schemas
ジム名取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


class GymInfo(BaseModel):
    """
    ジム情報スキーマ
    """

    gym_name: str = Field(..., description="ジム名称", example="CRUX大阪")
    gym_id: int = Field(..., description="ジムID", example=2)

    class Config:
        from_attributes = True


class GymsNameResponse(BaseModel):
    """
    ジム名取得APIのレスポンススキーマ
    """

    gyms_info: List[GymInfo] = Field(..., description="ジム名一覧")

    class Config:
        from_attributes = True
