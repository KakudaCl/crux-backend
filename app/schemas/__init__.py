"""
Schemas Package
Pydanticスキーマの定義
"""

from app.schemas.challenges import (
    ChallengeBase,
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeResponse
)
from app.schemas.top_rates import (
    MonthlyInfo,
    GradeTopRate,
    TopRateResponse
)
from app.schemas.area_top_rates import (
    AreaInfo,
    GradeAreaTopRate,
    AreaTopRateResponse
)

__all__ = [
    # Challenges schemas
    "ChallengeBase",
    "ChallengeCreate",
    "ChallengeUpdate",
    "ChallengeResponse",
    # Top Rates schemas
    "MonthlyInfo",
    "GradeTopRate",
    "TopRateResponse",
    # Area Top Rates schemas
    "AreaInfo",
    "GradeAreaTopRate",
    "AreaTopRateResponse",
]
