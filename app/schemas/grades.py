"""
Grades Schemas
グレード名取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List


class GradeInfo(BaseModel):
    """
    グレード情報スキーマ
    """

    grade_name: str = Field(..., description="グレード名", example="7Q")
    grade_id: int = Field(..., description="グレードID", example=4)

    class Config:
        from_attributes = True


class GradesNameResponse(BaseModel):
    """
    グレード名取得APIのレスポンススキーマ
    """

    grades_info: List[GradeInfo] = Field(..., description="グレード名一覧")

    class Config:
        from_attributes = True
