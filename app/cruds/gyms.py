"""
Gyms CRUD
ジム名取得APIのDB処理
"""

from sqlalchemy.orm import Session

from app import schemas
from app.models.gym_info import GymInfo


def get_gyms_name(db: Session) -> schemas.GymsNameResponse:
    """
    ジム情報テーブルからgym_idとgym_nameを一通り取得する。
    """
    gym_records = (
        db.query(GymInfo.gym_id, GymInfo.gym_name)
        .order_by(GymInfo.gym_id)
        .all()
    )

    gyms_info = [
        schemas.GymInfo(gym_id=gym_id, gym_name=gym_name)
        for gym_id, gym_name in gym_records
    ]

    return schemas.GymsNameResponse(gyms_info=gyms_info)
