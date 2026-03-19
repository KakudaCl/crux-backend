"""
Results CRUD
トライ結果名取得APIのDB処理
"""

from sqlalchemy.orm import Session

from app import schemas
from app.models.result_info import ResultInfo


def get_results_name(db: Session) -> schemas.ResultsNameResponse:
    """
    トライ結果情報テーブルからresult_idとresult_nameを一通り取得する。
    """
    result_records = (
        db.query(ResultInfo.result_id, ResultInfo.result_name)
        .order_by(ResultInfo.result_id)
        .all()
    )

    results_info = [
        schemas.ResultInfo(result_id=result_id, result_name=result_name)
        for result_id, result_name in result_records
    ]

    return schemas.ResultsNameResponse(results_info=results_info)
