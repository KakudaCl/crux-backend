"""
Challenges Router
挑戦記録APIのルーター定義
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.post("/challenges", response_model=schemas.ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge: schemas.ChallengeCreate,
    db: Session = Depends(get_db)
):
    """
    新しい挑戦記録を作成する
    """
    db_challenge = models.Challenge(**challenge.model_dump())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


@router.get("/challenges", response_model=List[schemas.ChallengeResponse])
async def get_challenges(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    user_name: Optional[str] = Query(None, description="挑戦者名でフィルタ"),
    grade: Optional[str] = Query(None, description="グレードでフィルタ"),
    success: Optional[bool] = Query(None, description="成功/失敗でフィルタ"),
    db: Session = Depends(get_db)
):
    """
    挑戦記録の一覧を取得する（フィルタリング・ページネーション対応）
    """
    query = db.query(models.Challenge)
    
    # フィルタリング
    if user_name:
        query = query.filter(models.Challenge.user_name.contains(user_name))
    if grade:
        query = query.filter(models.Challenge.grade == grade)
    if success is not None:
        query = query.filter(models.Challenge.success == success)
    
    # 新しい順にソート
    query = query.order_by(models.Challenge.created_at.desc())
    
    # ページネーション
    challenges = query.offset(skip).limit(limit).all()
    return challenges


@router.get("/challenges/{challenge_id}", response_model=schemas.ChallengeResponse)
async def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    """
    特定の挑戦記録を取得する
    """
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません"
        )
    return challenge


@router.put("/challenges/{challenge_id}", response_model=schemas.ChallengeResponse)
async def update_challenge(
    challenge_id: int,
    challenge_update: schemas.ChallengeUpdate,
    db: Session = Depends(get_db)
):
    """
    挑戦記録を更新する
    """
    db_challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if db_challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません"
        )
    
    # 更新データを適用
    update_data = challenge_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


@router.delete("/challenges/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    """
    挑戦記録を削除する
    """
    db_challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if db_challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {challenge_id} の挑戦記録が見つかりません"
        )
    
    db.delete(db_challenge)
    db.commit()
    return None


@router.get("/challenges/stats/summary")
async def get_stats_summary(
    user_name: Optional[str] = Query(None, description="特定ユーザーの統計を取得"),
    db: Session = Depends(get_db)
):
    """
    挑戦記録の統計情報を取得する
    """
    query = db.query(models.Challenge)
    
    if user_name:
        query = query.filter(models.Challenge.user_name == user_name)
    
    all_challenges = query.all()
    total_challenges = len(all_challenges)
    successful_challenges = sum(1 for c in all_challenges if c.success)
    success_rate = (successful_challenges / total_challenges * 100) if total_challenges > 0 else 0
    
    return {
        "total_challenges": total_challenges,
        "successful_challenges": successful_challenges,
        "failed_challenges": total_challenges - successful_challenges,
        "success_rate": round(success_rate, 2)
    }
