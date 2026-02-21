"""
Schemas Package
Pydanticスキーマの定義
"""

from app.schemas.top_rates import (
    MonthlyInfo,
    GradeTopRate,
    TopRateResponse,
    AreaInfo,
    GradeAreaTopRate,
    AreaTopRateResponse,
)
from app.schemas.trylogs import TryLogItem, DailyTryLog, TryLogResponse
from app.schemas.gyms import GymInfo, GymsNameResponse

__all__ = [
    # top_rate schemas
    "MonthlyInfo",
    "GradeTopRate",
    "TopRateResponse",
    "AreaInfo",
    "GradeAreaTopRate",
    "AreaTopRateResponse",
    # trylog schemas
    "TryLogItem",
    "DailyTryLog",
    "TryLogResponse",
    # gyms schemas
    "GymInfo",
    "GymsNameResponse",
]
