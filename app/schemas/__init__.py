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
    BestProbItem,
    BestProbResponse,
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
    # best prob schemas
    "BestProbItem",
    "BestProbResponse",
    # gyms schemas
    "GymInfo",
    "GymsNameResponse",
]
