"""
Gyms Router
ジム名取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import gyms as gyms_crud

router = APIRouter()


@router.get(
    "/gyms_name",
    summary="ジム名取得",
    response_model=schemas.GymsNameResponse,
    status_code=status.HTTP_200_OK,
)
async def get_gyms_name(
    db: Session = Depends(get_db),
):
    """
    ジム名を一通り取得する
    """
    try:
        return gyms_crud.get_gyms_name(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
