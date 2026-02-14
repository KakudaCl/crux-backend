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

    grade_mapping = db.query(GradeInfo.grade_id, GradeInfo.grade_name, GradeInfo.grade_color).all()
    grade_dict = {gid: {"grade_name": gname, "grade_color": gcolor} for gid, gname, gcolor in grade_mapping}

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
        grade_info = grade_dict.get(grade_id, {"grade_name": f"グレードID:{grade_id}", "grade_color": "000000"})
        grade_name = grade_info["grade_name"]
        grade_color = grade_info["grade_color"]
        monthly_info: List[schemas.MonthlyInfo] = []
        first_half_total = 0
        first_half_top = 0
        second_half_total = 0
        second_half_top = 0

        # 1-12月すべてを含める
        for month in range(1, 13):
            data = grade_month_data[grade_id].get(
                month, {"total": 0, "top": 0}
            )
            boulder_count = data["total"]
            top_count = data["top"]

            # データが存在しない月はtop_rateをNoneに設定
            if boulder_count > 0:
                top_rate = round((top_count / boulder_count * 100), 2)
            else:
                top_rate = None

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

        # 上半期・下半期・年間は必ず含める（データがなくても項目を返す）
        first_half_rate = (
            round((first_half_top / first_half_total * 100), 2)
            if first_half_total > 0
            else None
        )
        monthly_info.append(
            schemas.MonthlyInfo(
                month="上半期",
                top_rate=first_half_rate,
                boulder_count=first_half_total,
                top_count=first_half_top,
            )
        )
        second_half_rate = (
            round((second_half_top / second_half_total * 100), 2)
            if second_half_total > 0
            else None
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
        annual_rate = (
            round((annual_top / annual_total * 100), 2)
            if annual_total > 0
            else None
        )
        monthly_info.append(
            schemas.MonthlyInfo(
                month="年間",
                top_rate=annual_rate,
                boulder_count=annual_total,
                top_count=annual_top,
            )
        )
        result_info.append(
            schemas.GradeTopRate(grade=grade_name, grade_color=grade_color, monthly_info=monthly_info)
        )

    return schemas.TopRateResponse(result_info=result_info)
