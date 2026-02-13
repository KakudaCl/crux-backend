"""
Try Logs Schemas
トライログ取得APIのスキーマ定義
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class TryLogItem(BaseModel):
    """
    トライログの個別項目スキーマ
    """
    prob_no: str = Field(..., description="課題番号（例: No.1）")
    result: Optional[str] = Field(
        None, description="トライ結果（FLASH/TOP/ZONE/N.S.）"
    )
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
