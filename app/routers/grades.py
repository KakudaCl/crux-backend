"""
Grades Router
グレード名取得APIのルーター定義
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.cruds import grades as grades_crud

router = APIRouter(prefix="/api", tags=["共通"])

DbDep = Annotated[Session, Depends(get_db)]


@router.get(
    "/grade/list",
    summary="グレード名取得",
    response_model=schemas.GradesNameResponse,
    status_code=status.HTTP_200_OK,
)
def get_grades_name(
    gym_id: Annotated[int, Query(description="ジムID", example=1)],
    db: DbDep,
):
    """
    ジムIDからそのジムのグレード名を一通り取得する
    """
    try:
        return grades_crud.get_grades_name(db, gym_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}",
        )
