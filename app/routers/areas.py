"""
Areas Router
エリア名取得APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import areas as areas_crud

router = APIRouter()


@router.get(
    "/area/list",
    summary="エリア名取得",
    response_model=schemas.AreasNameResponse,
    status_code=status.HTTP_200_OK,
)
async def get_areas_name(
    gym_id: int = Query(..., description="ジムID", example=3),
    db: Session = Depends(get_db),
):
    """
    ジムIDからそのジムのエリア名を一通り取得する
    """
    try:
        return areas_crud.get_areas_name(db, gym_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
