"""
Try Logs / Top Rates CRUD
トライログ・完登率取得APIのDB処理
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_, or_
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import date, datetime

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo
from app.models.area_info import AreaInfo
from app.models.area_info import AreaInfo as AreaInfoModel


def delete_trylog(db: Session, try_id: int) -> None:
    """
    指定されたトライIDのトライ記録を論理削除する。

    is_deleted を 1 に設定し、deleted_at に現在時刻を格納する。
    対象レコードが存在しない場合は None を返す。
    """
    record = db.query(TryRecord).filter(TryRecord.try_id == try_id).first()
    if record is None:
        return None

    record.is_deleted = 1
    record.deleted_at = datetime.now()
    db.commit()
    return record


def get_years(db: Session) -> schemas.YearsResponse:
    """
    トライ記録テーブルからデータが存在する年度を一通り取得する。
    """
    year_records = (
        db.query(extract("year", TryRecord.try_date))
        .distinct()
        .order_by(extract("year", TryRecord.try_date))
        .all()
    )

    years = [int(year) for (year,) in year_records]
    return schemas.YearsResponse(years=years)


def register_trylog(db: Session, request: schemas.TryLogRegisterRequest) -> None:
    """
    トライログを登録・更新する。

    trylog_list の各アイテムに対して、try_date・gym_id・prob_no が一致する
    既存レコードがあれば上書き更新し、なければ新規登録する。
    prob_no が null の場合は常に新規登録する。
    """
    for item in request.trylog_list:
        existing = None
        if item.prob_no is not None:
            existing = (
                db.query(TryRecord)
                .filter(
                    TryRecord.try_date == request.try_date,
                    TryRecord.gym_id == request.gym_id,
                    TryRecord.problem_number == item.prob_no,
                )
                .first()
            )

        if existing:
            existing.grade_id = item.grade_id
            existing.result_id = item.result_id
            existing.area_id = item.area_id
            existing.day_count = item.day_count
            existing.remarks = item.remarks
        else:
            new_record = TryRecord(
                gym_id=request.gym_id,
                try_date=request.try_date,
                problem_number=item.prob_no,
                grade_id=item.grade_id,
                result_id=item.result_id,
                area_id=item.area_id,
                day_count=item.day_count,
                remarks=item.remarks,
            )
            db.add(new_record)

    db.commit()


def get_trylogs(
    db: Session, year: int, month: int, gym_id: int, sort: str = "prob_no"
) -> schemas.TryLogResponse:
    """
    年度・月・ジムIDを指定してトライログ情報を取得する。

    sort='prob_no': 日付グループ内を課題番号昇順でソート
    sort='time':    日付グループ内を登録日時(created_at)昇順でソート
    """
    if sort == "time":
        order_columns = [TryRecord.created_at.asc(), TryRecord.try_id.asc()]
    else:
        order_columns = [TryRecord.problem_number.asc(), TryRecord.try_id.asc()]

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
            TryRecord.is_deleted == 0,
        )
        .order_by(*order_columns)
        .all()
    )

    if not try_records:
        return schemas.TryLogResponse(all_logs=[])

    # try_date ごとにレコードをグルーピング（挿入順を保持するため OrderedDict 的に扱う）
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


def get_monthly_top_rates(
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
            TryRecord.is_deleted == 0,
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
                TryRecord.is_deleted == 0,
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


def get_best_prob(
    db: Session, year: int, gym_id: int, month: int
) -> schemas.BestProbResponse:
    """
    年度・月・ジムIDを指定してベスト完登課題を取得する。

    season_best: 指定年度の1月〜指定月・ジムでFLASH/TOPの中で最大課題番号のレコード
    personal_best: 指定年月以前の全期間・ジムでFLASH/TOPの中で最大課題番号のレコード
    同一最大課題番号が複数存在する場合は最も古い日付のレコードを返す。
    """
    COMPLETED_RESULT_IDS = [1, 2]  # 1: FLASH, 2: TOP

    season_record = (
        db.query(TryRecord)
        .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
        .filter(
            extract("year", TryRecord.try_date) == year,
            extract("month", TryRecord.try_date) <= month,
            TryRecord.gym_id == gym_id,
            TryRecord.result_id.in_(COMPLETED_RESULT_IDS),
            TryRecord.problem_number.isnot(None),
            TryRecord.is_deleted == 0,
        )
        .order_by(TryRecord.problem_number.desc(), TryRecord.try_date.asc())
        .first()
    )

    season_best = (
        schemas.BestProbItem(
            prob_no=season_record.problem_number,
            grade=season_record.grade.grade_name,
            grade_color=season_record.grade.grade_color,
            record_date=season_record.try_date,
        )
        if season_record
        else None
    )

    personal_record = (
        db.query(TryRecord)
        .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
        .filter(
            or_(
                extract("year", TryRecord.try_date) < year,
                and_(
                    extract("year", TryRecord.try_date) == year,
                    extract("month", TryRecord.try_date) <= month,
                ),
            ),
            TryRecord.gym_id == gym_id,
            TryRecord.result_id.in_(COMPLETED_RESULT_IDS),
            TryRecord.problem_number.isnot(None),
        )
        .order_by(TryRecord.problem_number.desc(), TryRecord.try_date.asc())
        .first()
    )

    personal_best = (
        schemas.BestProbItem(
            prob_no=personal_record.problem_number,
            grade=personal_record.grade.grade_name,
            grade_color=personal_record.grade.grade_color,
            record_date=personal_record.try_date,
        )
        if personal_record
        else None
    )

    return schemas.BestProbResponse(
        season_best=season_best,
        personal_best=personal_best,
    )


def _build_best_count_item(
    records: List[TryRecord], db: Session
) -> Optional[schemas.BestCountItem]:
    """
    FLASH/TOP レコードの中から最大 grade_id を持つ日付ごとの完登数を集計し、
    最多完登数の日付（同数の場合は最古の日付）を返す。
    """
    if not records:
        return None

    max_grade_id = max(r.grade_id for r in records)
    by_grade = [r for r in records if r.grade_id == max_grade_id]

    date_count: Dict[date, int] = defaultdict(int)
    for r in by_grade:
        date_count[r.try_date] += 1

    max_count = max(date_count.values())
    best_date = min(d for d, c in date_count.items() if c == max_count)

    grade_info = db.query(GradeInfo).filter(GradeInfo.grade_id == max_grade_id).first()

    return schemas.BestCountItem(
        grade=grade_info.grade_name,
        grade_color=grade_info.grade_color,
        top_count=max_count,
        record_date=best_date,
    )


def get_best_count(
    db: Session, year: int, gym_id: int, month: int
) -> schemas.BestCountResponse:
    """
    年度・月・ジムIDを指定してベスト完登数を取得する。

    season_best: 指定年度の1月〜指定月・ジムでFLASH/TOPの中で最大 grade_id を持ち、
                 1日あたりの完登数が最多の記録。
    personal_best: 指定年月以前の全期間・ジムで同様の条件で算出した記録。
    同一最多完登数の日付が複数存在する場合は最古の日付を選択する。
    """
    COMPLETED_RESULT_IDS = [1, 2]  # 1: FLASH, 2: TOP

    season_records = (
        db.query(TryRecord)
        .filter(
            extract("year", TryRecord.try_date) == year,
            extract("month", TryRecord.try_date) <= month,
            TryRecord.gym_id == gym_id,
            TryRecord.result_id.in_(COMPLETED_RESULT_IDS),
            TryRecord.is_deleted == 0,
        )
        .all()
    )

    personal_records = (
        db.query(TryRecord)
        .filter(
            or_(
                extract("year", TryRecord.try_date) < year,
                and_(
                    extract("year", TryRecord.try_date) == year,
                    extract("month", TryRecord.try_date) <= month,
                ),
            ),
            TryRecord.gym_id == gym_id,
            TryRecord.result_id.in_(COMPLETED_RESULT_IDS),
            TryRecord.is_deleted == 0,
        )
        .all()
    )

    return schemas.BestCountResponse(
        season_best=_build_best_count_item(season_records, db),
        personal_best=_build_best_count_item(personal_records, db),
    )
