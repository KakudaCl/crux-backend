"""
Try Logs Router
トライログ取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import trylogs as trylogs_crud

router = APIRouter()


@router.get(
    "/trylog",
    summary="トライログ取得",
    response_model=schemas.TryLogResponse,
    status_code=status.HTTP_200_OK,
)
async def get_trylogs(
    year: int = Query(..., description="年度", example=2026),
    month: int = Query(..., description="月", example=3),
    gym_id: int = Query(..., description="ジムID", example=1),
    db: Session = Depends(get_db),
):
    """
    年度/ジム/月別のトライログ情報を取得する
    """
    # パラメータバリデーション
    if year < 2000 or year > 2100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年度は2000〜2100の範囲で指定してください",
        )
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="月は1〜12の範囲で指定してください",
        )
    if gym_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ジムIDは1以上の値を指定してください",
        )

    try:
        return trylogs_crud.get_trylogs(
            db, year=year, month=month, gym_id=gym_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
