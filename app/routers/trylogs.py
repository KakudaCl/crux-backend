"""
Try Logs / Top Rates Router
トライログ・完登率取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import trylogs as trylogs_crud

router = APIRouter()


@router.post(
    "/trylog/register",
    summary="トライログ登録",
    status_code=status.HTTP_200_OK,
)
async def register_trylog(
    request: schemas.TryLogRegisterRequest = Body(...),
    db: Session = Depends(get_db),
):
    """
    トライログ情報を登録、更新する。

    trylog_list の各アイテムを try_record テーブルに登録する。
    try_date・gym_id・prob_no が一致するレコードが既に存在する場合は上書き更新する。
    """
    if not request.trylog_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="trylog_list は1件以上指定してください",
        )
    if request.gym_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ジムIDは1以上の値を指定してください",
        )
    try:
        trylogs_crud.register_trylog(db, request=request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/trylog/list",
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
        return trylogs_crud.get_trylogs(db, year=year, month=month, gym_id=gym_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/top_rate/month",
    summary="マンスリー別完登率取得",
    response_model=schemas.TopRateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_monthly_top_rates(
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
        return trylogs_crud.get_monthly_top_rates(db, year=year, gym_id=gym_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/top_rate/area",
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
        return trylogs_crud.get_area_top_rates(
            db, year=year, period=period, gym_id=gym_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/trylog/best/prob",
    summary="ベスト完登課題取得",
    response_model=schemas.BestProbResponse,
    status_code=status.HTTP_200_OK,
)
async def get_best_prob(
    year: int = Query(..., description="年度", example=2026),
    gym_id: int = Query(..., description="ジムID", example=1),
    month: int = Query(..., description="月", example=3),
    db: Session = Depends(get_db),
):
    """
    完登課題のベスト記録（シーズンベスト・パーソナルベスト）を取得する
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
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="月は1〜12の範囲で指定してください",
        )
    try:
        return trylogs_crud.get_best_prob(db, year=year, gym_id=gym_id, month=month)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/trylog/best/count",
    summary="ベスト完登数取得",
    response_model=schemas.BestCountResponse,
    status_code=status.HTTP_200_OK,
)
async def get_best_count(
    year: int = Query(..., description="年度", example=2026),
    gym_id: int = Query(..., description="ジムID", example=1),
    month: int = Query(..., description="月", example=4),
    db: Session = Depends(get_db),
):
    """
    完登数のベスト記録（シーズンベスト・パーソナルベスト）を取得する
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
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="月は1〜12の範囲で指定してください",
        )
    try:
        return trylogs_crud.get_best_count(db, year=year, gym_id=gym_id, month=month)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
