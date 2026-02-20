"""
Top Rates Router
完登率取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import top_rates as top_rates_crud

router = APIRouter()


@router.get(
    "/top_rates",
    summary="完登率取得",
    response_model=schemas.TopRateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_top_rates(
    year: int = Query(..., description="年度", example=2026),
    gym_id: int = Query(..., description="ジムID", example=1),
    db: Session = Depends(get_db),
):
    """
    年度/ジム/グレード別の完登率情報を取得する
    """
    if year < 2000 or year > 2100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年度は2000〜2100の範囲で指定してください",
        )
    if gym_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ジムIDは1以上の値を指定してください",
        )
    try:
        return top_rates_crud.get_top_rates(db, year=year, gym_id=gym_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/top_rates_area",
    summary="エリア別完登率取得",
    response_model=schemas.AreaTopRateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_area_top_rates(
    year: int = Query(..., description="年度", example=2026),
    period: int = Query(
        ..., description="期間（1:上半期、2:下半期、3:年間）", example=3
    ),
    gym_id: int = Query(..., description="ジムID", example=1),
    db: Session = Depends(get_db),
):
    """
    年度/ジム/グレード別の完登率情報(エリア別)を取得する
    """
    if year < 2000 or year > 2100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年度は2000〜2100の範囲で指定してください",
        )
    if period not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="期間は1（上半期）、2（下半期）、3（年間）のいずれかを指定してください",
        )
    if gym_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ジムIDは1以上の値を指定してください",
        )
    try:
        return top_rates_crud.get_area_top_rates(
            db, year=year, period=period, gym_id=gym_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
