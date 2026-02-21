"""
Try Logs / Top Rates CRUD
トライログ・完登率取得APIのDB処理
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from typing import Dict, List
from collections import defaultdict
from datetime import date

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo
from app.models.area_info import AreaInfo
from app.models.area_info import AreaInfo as AreaInfoModel


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


def get_top_rates(db: Session, year: int, gym_id: int) -> schemas.TopRateResponse:
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

    grade_mapping = db.query(
        GradeInfo.grade_id, GradeInfo.grade_name, GradeInfo.grade_color
    ).all()
    grade_dict = {
        gid: {"grade_name": gname, "grade_color": gcolor}
        for gid, gname, gcolor in grade_mapping
    }

    grade_month_data: Dict[int, Dict[int, Dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"total": 0, "top": 0})
    )

    for record in try_records:
        grade_id = record.grade_id
        month = record.try_date.month
        result_name = record.result.result_name
        grade_month_data[grade_id][month]["total"] += 1
        if result_name in ["FLASH", "TOP"]:
            grade_month_data[grade_id][month]["top"] += 1

    result_info: List[schemas.GradeTopRate] = []

    for grade_id in sorted(grade_month_data.keys()):
        grade_info = grade_dict.get(
            grade_id, {"grade_name": f"グレードID:{grade_id}", "grade_color": "000000"}
        )
        grade_name = grade_info["grade_name"]
        grade_color = grade_info["grade_color"]
        monthly_info: List[schemas.MonthlyInfo] = []
        first_half_total = 0
        first_half_top = 0
        second_half_total = 0
        second_half_top = 0

        for month in range(1, 13):
            data = grade_month_data[grade_id].get(month, {"total": 0, "top": 0})
            boulder_count = data["total"]
            top_count = data["top"]

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
            round((annual_top / annual_total * 100), 2) if annual_total > 0 else None
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
            schemas.GradeTopRate(
                grade=grade_name, grade_color=grade_color, monthly_info=monthly_info
            )
        )

    return schemas.TopRateResponse(result_info=result_info)


def get_area_top_rates(
    db: Session, year: int, period: int, gym_id: int
) -> schemas.AreaTopRateResponse:
    """
    年度・期間・ジムIDを指定してエリア別完登率情報を取得する。

    Args:
        db: データベースセッション
        year: 年度
        period: 期間 (1:上半期、2:下半期、3:年間)
        gym_id: ジムID

    Returns:
        エリア別完登率情報
    """
    if period == 1:
        month_range = range(1, 7)
    elif period == 2:
        month_range = range(7, 13)
    else:
        month_range = range(1, 13)

    try_records = (
        db.query(TryRecord)
        .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
        .join(ResultInfo, TryRecord.result_id == ResultInfo.result_id)
        .join(AreaInfoModel, TryRecord.area_id == AreaInfoModel.area_id)
        .filter(
            and_(
                extract("year", TryRecord.try_date) == year,
                extract("month", TryRecord.try_date).in_(month_range),
                TryRecord.gym_id == gym_id,
            )
        )
        .all()
    )

    if not try_records:
        return schemas.AreaTopRateResponse(result_info=[])

    grade_mapping = db.query(
        GradeInfo.grade_id, GradeInfo.grade_name, GradeInfo.grade_color
    ).all()
    grade_dict = {
        gid: {"grade_name": gname, "grade_color": gcolor}
        for gid, gname, gcolor in grade_mapping
    }

    area_mapping = (
        db.query(AreaInfoModel.area_id, AreaInfoModel.area_name)
        .filter(AreaInfoModel.gym_id == gym_id)
        .order_by(AreaInfoModel.area_id)
        .all()
    )
    area_dict = {aid: aname for aid, aname in area_mapping}
    all_area_ids = [aid for aid, _ in area_mapping]

    grade_area_data: Dict[int, Dict[int, Dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"total": 0, "top": 0})
    )

    for record in try_records:
        grade_id = record.grade_id
        area_id = record.area_id
        result_name = record.result.result_name

        grade_area_data[grade_id][area_id]["total"] += 1
        if result_name in ["FLASH", "TOP"]:
            grade_area_data[grade_id][area_id]["top"] += 1

    result_info: List[schemas.GradeAreaTopRate] = []

    for grade_id in sorted(grade_area_data.keys()):
        grade_info = grade_dict.get(
            grade_id, {"grade_name": f"グレードID:{grade_id}", "grade_color": "000000"}
        )
        grade_name = grade_info["grade_name"]
        grade_color = grade_info["grade_color"]
        area_info_list: List[schemas.AreaInfo] = []

        for area_id in all_area_ids:
            area_name = area_dict.get(area_id, f"エリアID:{area_id}")
            data = grade_area_data[grade_id].get(area_id, {"total": 0, "top": 0})
            boulder_count = data["total"]
            top_count = data["top"]

            if boulder_count == 0:
                area_info_list.append(
                    schemas.AreaInfo(
                        area_name=area_name,
                        top_rate=None,
                        boulder_count=0,
                        top_count=0,
                    )
                )
            else:
                top_rate = round((top_count / boulder_count * 100), 2)
                area_info_list.append(
                    schemas.AreaInfo(
                        area_name=area_name,
                        top_rate=top_rate,
                        boulder_count=boulder_count,
                        top_count=top_count,
                    )
                )

        result_info.append(
            schemas.GradeAreaTopRate(
                grade=grade_name, grade_color=grade_color, area_info=area_info_list
            )
        )

    return schemas.AreaTopRateResponse(result_info=result_info)
