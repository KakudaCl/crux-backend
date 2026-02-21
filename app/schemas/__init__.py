"""
Schemas Package
Pydanticスキーマの定義
"""

from app.schemas.trylogs import (
    TryLogItem,
    DailyTryLog,
    TryLogResponse,
    MonthlyInfo,
    GradeTopRate,
    TopRateResponse,
    AreaInfo,
    GradeAreaTopRate,
    AreaTopRateResponse,
)
from app.schemas.gyms import GymInfo, GymsNameResponse

__all__ = [
    # trylog schemas
    "TryLogItem",
    "DailyTryLog",
    "TryLogResponse",
    # top_rate schemas
    "MonthlyInfo",
    "GradeTopRate",
    "TopRateResponse",
    "AreaInfo",
    "GradeAreaTopRate",
    "AreaTopRateResponse",
    # gyms schemas
    "GymInfo",
    "GymsNameResponse",
]
