"""
Challenges Router
挑戦記録APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas
from app.database import get_db
from app.cruds import challenges as challenges_crud

router = APIRouter()


@router.post(
    "/challenges",
    summary="挑戦記録作成",
    response_model=schemas.ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_challenge(
    challenge: schemas.ChallengeCreate,
    db: Session = Depends(get_db),
):
    """新しい挑戦記録を作成する。"""
    return challenges_crud.create_challenge(db, challenge)


@router.get(
    "/challenges",
    summary="挑戦記録一覧取得",
    response_model=List[schemas.ChallengeResponse],
)
async def get_challenges(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    user_name: Optional[str] = Query(None, description="挑戦者名でフィルタ"),
    grade: Optional[str] = Query(None, description="グレードでフィルタ"),
    success: Optional[bool] = Query(None, description="成功/失敗でフィルタ"),
    db: Session = Depends(get_db),
):
    """挑戦記録の一覧を取得する（フィルタリング・ページネーション対応）。"""
    return challenges_crud.get_challenges(
        db, skip=skip, limit=limit,
        user_name=user_name, grade=grade, success=success,
    )


@router.get(
    "/challenges/{challenge_id}",
    summary="挑戦記録1件取得",
    response_model=schemas.ChallengeResponse,
)
async def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    """特定の挑戦記録を取得する。"""
    challenge = challenges_crud.get_challenge(db, challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません",
        )
    return challenge


@router.put(
    "/challenges/{challenge_id}",
    summary="挑戦記録更新",
    response_model=schemas.ChallengeResponse,
)
async def update_challenge(
    challenge_id: int,
    challenge_update: schemas.ChallengeUpdate,
    db: Session = Depends(get_db),
):
    """挑戦記録を更新する。"""
    db_challenge = challenges_crud.update_challenge(
        db, challenge_id, challenge_update
    )
    if db_challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません",
        )
    return db_challenge


@router.delete(
    "/challenges/{challenge_id}",
    summary="挑戦記録削除",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    """挑戦記録を削除する。"""
    if not challenges_crud.delete_challenge(db, challenge_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません",
        )
    return None


@router.get(
    "/challenges/stats/summary",
    summary="挑戦記録統計取得",
)
async def get_stats_summary(
    user_name: Optional[str] = Query(
        None, description="特定ユーザーの統計を取得"
    ),
    db: Session = Depends(get_db),
):
    """挑戦記録の統計情報を取得する。"""
    return challenges_crud.get_stats_summary(db, user_name=user_name)
