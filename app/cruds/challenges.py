"""
Challenges CRUD
挑戦記録APIのDB処理
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas


def create_challenge(
    db: Session, challenge: schemas.ChallengeCreate
) -> models.Challenge:
    """挑戦記録を1件作成する。"""
    db_challenge = models.Challenge(**challenge.model_dump())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_challenges(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_name: Optional[str] = None,
    grade: Optional[str] = None,
    success: Optional[bool] = None,
) -> List[models.Challenge]:
    """挑戦記録の一覧を取得する（フィルタ・ページネーション対応）。"""
    query = db.query(models.Challenge)
    if user_name:
        query = query.filter(models.Challenge.user_name.contains(user_name))
    if grade:
        query = query.filter(models.Challenge.grade == grade)
    if success is not None:
        query = query.filter(models.Challenge.success == success)
    query = query.order_by(models.Challenge.created_at.desc())
    return query.offset(skip).limit(limit).all()


def get_challenge(
    db: Session, challenge_id: int
) -> Optional[models.Challenge]:
    """IDで挑戦記録を1件取得する。"""
    return (
        db.query(models.Challenge)
        .filter(models.Challenge.id == challenge_id)
        .first()
    )


def update_challenge(
    db: Session, challenge_id: int, challenge_update: schemas.ChallengeUpdate
) -> Optional[models.Challenge]:
    """挑戦記録を更新する。存在しない場合はNone。"""
    db_challenge = get_challenge(db, challenge_id)
    if db_challenge is None:
        return None
    update_data = challenge_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def delete_challenge(db: Session, challenge_id: int) -> bool:
    """挑戦記録を削除する。存在した場合はTrue、しなければFalse。"""
    db_challenge = get_challenge(db, challenge_id)
    if db_challenge is None:
        return False
    db.delete(db_challenge)
    db.commit()
    return True


def get_stats_summary(
    db: Session, user_name: Optional[str] = None
) -> dict:
    """挑戦記録の統計情報を取得する。"""
    query = db.query(models.Challenge)
    if user_name:
        query = query.filter(models.Challenge.user_name == user_name)
    all_challenges = query.all()
    total = len(all_challenges)
    successful = sum(1 for c in all_challenges if c.success)
    success_rate = (successful / total * 100) if total > 0 else 0
    return {
        "total_challenges": total,
        "successful_challenges": successful,
        "failed_challenges": total - successful,
        "success_rate": round(success_rate, 2),
    }
