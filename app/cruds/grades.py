"""
Grades CRUD
グレード名取得APIのDB処理
"""

from sqlalchemy.orm import Session

from app import schemas
from app.models.grade_info import GradeInfo


def get_grades_name(db: Session, gym_id: int) -> schemas.GradesNameResponse:
    """
    グレード情報テーブルからジムIDに対応するgrade_idとgrade_nameを一通り取得する。
    """
    grade_records = (
        db.query(GradeInfo.grade_id, GradeInfo.grade_name)
        .filter(GradeInfo.gym_id == gym_id)
        .order_by(GradeInfo.grade_id)
        .all()
    )

    grades_info = [
        schemas.GradeInfo(grade_id=grade_id, grade_name=grade_name)
        for grade_id, grade_name in grade_records
    ]

    return schemas.GradesNameResponse(grades_info=grades_info)
