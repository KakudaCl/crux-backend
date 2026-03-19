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
    BestCountItem,
    BestCountResponse,
    TryLogRegisterItem,
    TryLogRegisterRequest,
)
from app.schemas.gyms import GymInfo, GymsNameResponse
from app.schemas.grades import GradeInfo, GradesNameResponse
from app.schemas.areas import AreaNameItem, AreasNameResponse
from app.schemas.results import ResultInfo, ResultsNameResponse

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
    # best count schemas
    "BestCountItem",
    "BestCountResponse",
    # trylog register schemas
    "TryLogRegisterItem",
    "TryLogRegisterRequest",
    # gyms schemas
    "GymInfo",
    "GymsNameResponse",
    # grades schemas
    "GradeInfo",
    "GradesNameResponse",
    # areas schemas
    "AreaNameItem",
    "AreasNameResponse",
    # results schemas
    "ResultInfo",
    "ResultsNameResponse",
]
