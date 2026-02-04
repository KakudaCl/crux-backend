"""
Area Top Rates CRUD
エリア別完登率取得APIのDB処理
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from typing import Dict, List
from collections import defaultdict

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo
from app.models.area_info import AreaInfo as AreaInfoModel


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
    # 期間に応じた月の範囲を決定
    if period == 1:  # 上半期
        month_range = range(1, 7)
    elif period == 2:  # 下半期
        month_range = range(7, 13)
    else:  # 年間
        month_range = range(1, 13)

    # トライ記録を取得
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

    # グレード情報とエリア情報のマッピングを取得
    grade_mapping = db.query(GradeInfo.grade_id, GradeInfo.grade_name).all()
    grade_dict = {gid: gname for gid, gname in grade_mapping}

    # 対象ジムの全エリアを取得（仕様：全てのエリア名を項目として含める）
    area_mapping = (
        db.query(AreaInfoModel.area_id, AreaInfoModel.area_name)
        .filter(AreaInfoModel.gym_id == gym_id)
        .order_by(AreaInfoModel.area_id)
        .all()
    )
    area_dict = {aid: aname for aid, aname in area_mapping}
    all_area_ids = [aid for aid, _ in area_mapping]

    # グレード×エリアごとにデータを集計
    # 構造: {grade_id: {area_id: {"total": int, "top": int}}}
    grade_area_data: Dict[
        int, Dict[int, Dict[str, int]]
    ] = defaultdict(lambda: defaultdict(lambda: {"total": 0, "top": 0}))

    for record in try_records:
        grade_id = record.grade_id
        area_id = record.area_id
        result_name = record.result.result_name

        grade_area_data[grade_id][area_id]["total"] += 1
        if result_name in ["FLASH", "TOP"]:
            grade_area_data[grade_id][area_id]["top"] += 1

    # レスポンスを構築
    result_info: List[schemas.GradeAreaTopRate] = []

    for grade_id in sorted(grade_area_data.keys()):
        grade_name = grade_dict.get(grade_id, f"グレードID:{grade_id}")
        area_info_list: List[schemas.AreaInfo] = []

        # 全てのエリアを項目として含める（データがないエリアは top_rate=null, 件数=0）
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
                grade=grade_name,
                area_info=area_info_list
            )
        )

    return schemas.AreaTopRateResponse(result_info=result_info)
