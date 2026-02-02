"""
Top Rates API
完登率取得APIのエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Dict, List
from collections import defaultdict

from app import schemas
from app.models.try_record import TryRecord
from app.models.grade_info import GradeInfo
from app.models.result_info import ResultInfo
from app.database import get_db

router = APIRouter()


@router.get(
    "/top_rates",
    response_model=schemas.TopRateResponse,
    status_code=status.HTTP_200_OK
)
async def get_top_rates(
    year: int = Query(..., description="年度", example=2026),
    gym_id: int = Query(..., description="ジムID", example=1),
    db: Session = Depends(get_db)
):
    """
    完登率取得API

    年度/ジム/グレード別の完登率情報を取得する

    Parameters:
    - year: 年度（必須）
    - gym_id: ジムID（必須）

    Returns:
    - 完登率情報一覧（グレード別・月別）
    """

    try:
        # パラメータバリデーション
        if year < 1900 or year > 2100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="年度は1900〜2100の範囲で指定してください"
            )

        if gym_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ジムIDは1以上の値を指定してください"
            )

        # トライ記録を取得（年度とジムIDでフィルタ）
        try_records = (
            db.query(TryRecord)
            .join(GradeInfo, TryRecord.grade_id == GradeInfo.grade_id)
            .join(
                ResultInfo,
                TryRecord.result_id == ResultInfo.result_id
            )
            .filter(
                extract('year', TryRecord.try_date) == year,
                TryRecord.gym_id == gym_id
            )
            .all()
        )

        # データが存在しない場合は空の配列を返す
        if not try_records:
            return schemas.TopRateResponse(result_info=[])

        # グレードIDと名前のマッピングを取得
        grade_mapping = (
            db.query(GradeInfo.grade_id, GradeInfo.grade_name)
            .all()
        )
        grade_dict = {
            grade_id: grade_name
            for grade_id, grade_name in grade_mapping
        }

        # グレードID × 月 でグループ化してデータを集計
        # データ構造: {grade_id: {month: {"total": int, "top": int}}}
        grade_month_data: Dict[
            int, Dict[int, Dict[str, int]]
        ] = defaultdict(
            lambda: defaultdict(lambda: {"total": 0, "top": 0})
        )

        for record in try_records:
            grade_id = record.grade_id
            month = record.try_date.month
            result_name = record.result.result_name

            # 挑戦課題数をカウント
            grade_month_data[grade_id][month]["total"] += 1

            # 完登数をカウント（FLASHまたはTOP）
            if result_name in ["FLASH", "TOP"]:
                grade_month_data[grade_id][month]["top"] += 1

        # レスポンスデータの構築
        result_info: List[schemas.GradeTopRate] = []

        # グレードIDでソート（難易度順を想定）
        for grade_id in sorted(grade_month_data.keys()):
            grade_name = grade_dict.get(
                grade_id, f"グレードID:{grade_id}"
            )
            monthly_info: List[schemas.MonthlyInfo] = []

            # 月でソート
            for month in sorted(grade_month_data[grade_id].keys()):
                data = grade_month_data[grade_id][month]
                boulder_count = data["total"]
                top_count = data["top"]

                # 完登率を計算（小数第二位まで）
                if boulder_count > 0:
                    top_rate = round(
                        (top_count / boulder_count * 100), 2
                    )
                else:
                    top_rate = 0.0

                monthly_info.append(
                    schemas.MonthlyInfo(
                        month=f"{month}月",
                        top_rate=top_rate,
                        boulder_count=boulder_count,
                        top_count=top_count
                    )
                )

            result_info.append(
                schemas.GradeTopRate(
                    grade=grade_name,
                    monthly_info=monthly_info
                )
            )

        return schemas.TopRateResponse(result_info=result_info)

    except HTTPException:
        # HTTPExceptionはそのまま再送出
        raise
    except Exception as e:
        # その他のエラーは500エラーとして返す
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"内部処理エラーが発生しました: {str(e)}"
        )
