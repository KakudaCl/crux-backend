"""
Results Schemas
トライ結果名取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


class ResultInfo(BaseModel):
    """
    トライ結果情報スキーマ
    """

    result_name: str = Field(..., description="トライ結果名", example="FLASH")
    result_id: int = Field(..., description="トライ結果ID", example=1)

    class Config:
        from_attributes = True


class ResultsNameResponse(BaseModel):
    """
    トライ結果名取得APIのレスポンススキーマ
    """

    results_info: List[ResultInfo] = Field(..., description="トライ結果名一覧")

    class Config:
        from_attributes = True
