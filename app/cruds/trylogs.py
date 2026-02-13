"""
Try Logs CRUD
トライログ取得APIのDB処理
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List
from collections import defaultdict
from datetime import date

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo
from app.models.area_info import AreaInfo


def get_trylogs(
    db: Session, year: int, month: int, gym_id: int
) -> schemas.TryLogResponse:
    """
    年度・月・ジムIDを指定してトライログ情報を取得する。
    """
    # 指定された年度・月・ジムIDに一致するトライ記録を取得
    try_records = (
        db.query(TryRecord)
        .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
        .join(ResultInfo, TryRecord.result_id == ResultInfo.result_id)
        .outerjoin(AreaInfo, TryRecord.area_id == AreaInfo.area_id)
        .filter(
            extract("year", TryRecord.try_date) == year,
            extract("month", TryRecord.try_date) == month,
            TryRecord.gym_id == gym_id,
        )
        .order_by(TryRecord.try_date, TryRecord.try_id)
        .all()
    )

    if not try_records:
        return schemas.TryLogResponse(all_logs=[])

    # try_date ごとにレコードをグルーピング
    date_grouped: defaultdict[date, List[TryRecord]] = defaultdict(list)
    for record in try_records:
        date_grouped[record.try_date].append(record)

    # レスポンスの構築
    all_logs: List[schemas.DailyTryLog] = []

    for try_date in sorted(date_grouped.keys()):
        try_log_items: List[schemas.TryLogItem] = []

        for record in date_grouped[try_date]:
            # 課題番号の生成
            if record.problem_number is not None:
                prob_no = f"No.{record.problem_number}"
            else:
                prob_no = "No.-"

            # 結果名の取得
            result = record.result.result_name if record.result else None

            # エリア名の取得
            area = record.area.area_name if record.area else None

            # グレード色の取得
            grade_color = record.grade.grade_color if record.grade else None

            try_log_items.append(
                schemas.TryLogItem(
                    prob_no=prob_no,
                    result=result,
                    area=area,
                    day_count=record.day_count,
                    remarks=record.remarks,
                    grade_color=grade_color,
                )
            )

        all_logs.append(
            schemas.DailyTryLog(
                try_date=try_date,
                try_log=try_log_items,
            )
        )

    return schemas.TryLogResponse(all_logs=all_logs)
