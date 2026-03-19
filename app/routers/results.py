"""
Results Router
トライ結果名取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import results as results_crud

router = APIRouter()


@router.get(
    "/result/list",
    summary="トライ結果名取得",
    response_model=schemas.ResultsNameResponse,
    status_code=status.HTTP_200_OK,
)
async def get_results_name(
    db: Session = Depends(get_db),
):
    """
    トライ結果名を一通り取得する
    """
    try:
        return results_crud.get_results_name(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
