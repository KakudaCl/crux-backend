"""
Top Rates CRUD
完登率取得APIのDB処理
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Dict, List
from collections import defaultdict

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo


def get_top_rates(
    db: Session, year: int, gym_id: int
) -> schemas.TopRateResponse:
    """
    年度・ジムIDを指定して完登率情報を取得する。
    """
    try_records = (
        db.query(TryRecord)
        .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
        .join(ResultInfo, TryRecord.result_id == ResultInfo.result_id)
        .filter(
            extract("year", TryRecord.try_date) == year,
            TryRecord.gym_id == gym_id,
        )
        .all()
    )

    if not try_records:
        return schemas.TopRateResponse(result_info=[])

    grade_mapping = db.query(GradeInfo.grade_id, GradeInfo.grade_name).all()
    grade_dict = {gid: gname for gid, gname in grade_mapping}

    grade_month_data: Dict[
        int, Dict[int, Dict[str, int]]
    ] = defaultdict(lambda: defaultdict(lambda: {"total": 0, "top": 0}))

    for record in try_records:
        grade_id = record.grade_id
        month = record.try_date.month
        result_name = record.result.result_name
        grade_month_data[grade_id][month]["total"] += 1
        if result_name in ["FLASH", "TOP"]:
            grade_month_data[grade_id][month]["top"] += 1

    result_info: List[schemas.GradeTopRate] = []

    for grade_id in sorted(grade_month_data.keys()):
        grade_name = grade_dict.get(grade_id, f"グレードID:{grade_id}")
        monthly_info: List[schemas.MonthlyInfo] = []
        first_half_total = 0
        first_half_top = 0
        second_half_total = 0
        second_half_top = 0

        for month in sorted(grade_month_data[grade_id].keys()):
            data = grade_month_data[grade_id][month]
            boulder_count = data["total"]
            top_count = data["top"]
            top_rate = (
                round((top_count / boulder_count * 100), 2)
                if boulder_count > 0 else 0.0
            )
            monthly_info.append(
                schemas.MonthlyInfo(
                    month=f"{month}月",
                    top_rate=top_rate,
                    boulder_count=boulder_count,
                    top_count=top_count,
                )
            )
            if 1 <= month <= 6:
                first_half_total += boulder_count
                first_half_top += top_count
            elif 7 <= month <= 12:
                second_half_total += boulder_count
                second_half_top += top_count

        if first_half_total > 0:
            first_half_rate = round(
                (first_half_top / first_half_total * 100), 2
            )
            monthly_info.append(
                schemas.MonthlyInfo(
                    month="上半期",
                    top_rate=first_half_rate,
                    boulder_count=first_half_total,
                    top_count=first_half_top,
                )
            )
        if second_half_total > 0:
            second_half_rate = round(
                (second_half_top / second_half_total * 100), 2
            )
            monthly_info.append(
                schemas.MonthlyInfo(
                    month="下半期",
                    top_rate=second_half_rate,
                    boulder_count=second_half_total,
                    top_count=second_half_top,
                )
            )
        annual_total = first_half_total + second_half_total
        annual_top = first_half_top + second_half_top
        if annual_total > 0:
            annual_rate = round((annual_top / annual_total * 100), 2)
            monthly_info.append(
                schemas.MonthlyInfo(
                    month="年間",
                    top_rate=annual_rate,
                    boulder_count=annual_total,
                    top_count=annual_top,
                )
            )
        result_info.append(
            schemas.GradeTopRate(grade=grade_name, monthly_info=monthly_info)
        )

    return schemas.TopRateResponse(result_info=result_info)
