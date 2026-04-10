"""
Try Logs / Top Rates Router
トライログ・完登率取得APIのルーター定義
"""

from typing import Annotated, Literal

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import trylogs as trylogs_crud

router = APIRouter(prefix="/api", tags=["トライログ"])

DbDep = Annotated[Session, Depends(get_db)]


@router.get(
    "/trylog/year",
    summary="年度取得",
    status_code=status.HTTP_200_OK,
)
def get_years(
    db: DbDep,
) -> schemas.YearsResponse:
    """
    データが存在する年度を一通り取得する
    """
    try:
        return trylogs_crud.get_years(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.post(
    "/trylog/register",
    summary="トライログ登録",
    status_code=status.HTTP_200_OK,
)
def register_trylog(
    request: Annotated[schemas.TryLogRegisterRequest, Body()],
    db: DbDep,
) -> None:
    """
    トライログ情報を登録、更新する。

    trylog_list の各アイテムを try_record テーブルに登録する。
    try_date・gym_id・prob_no が一致するレコードが既に存在する場合は上書き更新する。
    """
    try:
        trylogs_crud.register_trylog(db, request=request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.post(
    "/trylog/edit",
    summary="トライログ編集",
    status_code=status.HTTP_200_OK,
)
def edit_trylog(
    request: Annotated[schemas.TryLogEditRequest, Body()],
    db: DbDep,
) -> None:
    """
    指定されたトライIDのトライログ情報を編集する。
    """
    try:
        result = trylogs_crud.edit_trylog(db, request=request)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"指定されたトライID（{request.try_id}）のレコードが存在しません",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.post(
    "/trylog/delete",
    summary="トライログ削除",
    status_code=status.HTTP_200_OK,
)
def delete_trylog(
    try_id: Annotated[int, Query(ge=1, description="トライID", example=341)],
    db: DbDep,
) -> None:
    """
    指定されたトライIDのトライログ情報を論理削除する。
    """
    try:
        result = trylogs_crud.delete_trylog(db, try_id=try_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"指定されたトライID（{try_id}）のレコードが存在しません",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/trylog/list",
    summary="トライログ取得",
    status_code=status.HTTP_200_OK,
)
def get_trylogs(
    year: Annotated[int, Query(ge=2000, le=2100, description="年度", example=2026)],
    month: Annotated[int, Query(ge=1, le=12, description="月", example=3)],
    gym_id: Annotated[int, Query(ge=1, description="ジムID", example=1)],
    db: DbDep,
    sort: Annotated[
        Literal["prob_no", "time"],
        Query(
            description="ソート順（'prob_no': 課題番号昇順 / 'time': 登録日時昇順）",
            example="prob_no",
        ),
    ] = "prob_no",
) -> schemas.TryLogResponse:
    """
    年度/ジム/月別のトライログ情報を取得する
    """
    try:
        return trylogs_crud.get_trylogs(
            db, year=year, month=month, gym_id=gym_id, sort=sort
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )


@router.get(
    "/top_rate/month",
    summary="マンスリー別完登率取得",
    status_code=status.HTTP_200_OK,
)
def get_monthly_top_rates(
    year: Annotated[int, Query(ge=2000, le=2100, description="年度", example=2026)],
    gym_id: Annotated[int, Query(ge=1, description="ジムID", example=1)],
    db: DbDep,
) -> schemas.TopRateResponse:
    """
    年度/ジム/グレード別の完登率情報を取得する
    """
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
    status_code=status.HTTP_200_OK,
)
def get_area_top_rates(
    year: Annotated[int, Query(ge=2000, le=2100, description="年度", example=2026)],
    period: Annotated[
        int,
        Query(ge=1, le=3, description="期間（1:上半期、2:下半期、3:年間）", example=3),
    ],
    gym_id: Annotated[int, Query(ge=1, description="ジムID", example=1)],
    db: DbDep,
) -> schemas.AreaTopRateResponse:
    """
    年度/ジム/グレード別の完登率情報(エリア別)を取得する
    """
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
    status_code=status.HTTP_200_OK,
)
def get_best_prob(
    year: Annotated[int, Query(ge=2000, le=2100, description="年度", example=2026)],
    gym_id: Annotated[int, Query(ge=1, description="ジムID", example=1)],
    month: Annotated[int, Query(ge=1, le=12, description="月", example=3)],
    db: DbDep,
) -> schemas.BestProbResponse:
    """
    完登課題のベスト記録（シーズンベスト・パーソナルベスト）を取得する
    """
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
    status_code=status.HTTP_200_OK,
)
def get_best_count(
    year: Annotated[int, Query(ge=2000, le=2100, description="年度", example=2026)],
    gym_id: Annotated[int, Query(ge=1, description="ジムID", example=1)],
    month: Annotated[int, Query(ge=1, le=12, description="月", example=4)],
    db: DbDep,
) -> schemas.BestCountResponse:
    """
    完登数のベスト記録（シーズンベスト・パーソナルベスト）を取得する
    """
    try:
        return trylogs_crud.get_best_count(db, year=year, gym_id=gym_id, month=month)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
