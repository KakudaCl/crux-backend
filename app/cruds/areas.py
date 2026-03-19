"""
Areas CRUD
エリア名取得APIのDB処理
"""

from sqlalchemy.orm import Session

from app import schemas
from app.models.area_info import AreaInfo


def get_areas_name(db: Session, gym_id: int) -> schemas.AreasNameResponse:
    """
    エリア情報テーブルからジムIDに対応するarea_idとarea_nameを一通り取得する。
    """
    area_records = (
        db.query(AreaInfo.area_id, AreaInfo.area_name)
        .filter(AreaInfo.gym_id == gym_id)
        .order_by(AreaInfo.area_id)
        .all()
    )

    areas_info = [
        schemas.AreaNameItem(area_id=area_id, area_name=area_name)
        for area_id, area_name in area_records
    ]

    return schemas.AreasNameResponse(areas_info=areas_info)
