"""
Try Logs / Top Rates Schemas
トライログ・完登率取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class TryLogItem(BaseModel):
    """
    トライログの個別項目スキーマ
    """

    prob_no: str = Field(..., description="課題番号（例: No.1）")
    result: Optional[str] = Field(None, description="トライ結果（FLASH/TOP/ZONE/N.S.）")
    area: Optional[str] = Field(None, description="エリア名（例: 垂壁）")
    day_count: Optional[int] = Field(None, description="トライ日数")
    remarks: Optional[str] = Field(None, description="備考")
    grade_color: Optional[str] = Field(None, description="グレード色（カラーコード）")

    class Config:
        from_attributes = True


class DailyTryLog(BaseModel):
    """
    日別トライログスキーマ
    """

    try_date: date = Field(..., description="トライ日（例: 2025-04-28）")
    try_log: List[TryLogItem] = Field(..., description="その日のトライログ一覧")

    class Config:
        from_attributes = True


class TryLogResponse(BaseModel):
    """
    トライログ取得APIのレスポンススキーマ
    """

    all_logs: List[DailyTryLog] = Field(..., description="トライログ一覧")

    class Config:
        from_attributes = True


class MonthlyInfo(BaseModel):
    """
    月別情報スキーマ
    """

    month: str = Field(..., description="月（例: 1月）")
    top_rate: Optional[float] = Field(
        ..., description="完登率（%）、データがない場合はnull"
    )
    boulder_count: int = Field(..., description="挑戦課題数")
    top_count: int = Field(..., description="完登数")

    class Config:
        from_attributes = True


class GradeTopRate(BaseModel):
    """
    グレード別完登率情報スキーマ
    """

    grade: str = Field(..., description="グレード名（例: 3級）")
    grade_color: str = Field(..., description="グレード色（カラーコード）")
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


class AreaInfo(BaseModel):
    """
    エリア別情報スキーマ
    データがないエリアも含め、全てのエリア名を項目として返す。
    """

    area_name: str = Field(..., description="エリア名（例: 強傾斜）")
    top_rate: Optional[float] = Field(
        None, description="完登率（%）。データがない場合はnull"
    )
    boulder_count: int = Field(0, description="挑戦課題数")
    top_count: int = Field(0, description="完登数")

    class Config:
        from_attributes = True


class GradeAreaTopRate(BaseModel):
    """
    グレード別エリア完登率情報スキーマ
    """

    grade: str = Field(..., description="グレード名（例: 3級）")
    grade_color: str = Field(..., description="グレード色（カラーコード）")
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
