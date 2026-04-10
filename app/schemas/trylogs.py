"""
Try Logs / Top Rates Schemas
トライログ・完登率取得APIのスキーマ定義
"""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TryLogItem(BaseModel):
    """
    トライログの個別項目スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    prob_no: str = Field(description="課題番号（例: No.1）")
    result: str | None = Field(None, description="トライ結果（FLASH/TOP/ZONE/N.S.）")
    area: str | None = Field(None, description="エリア名（例: 垂壁）")
    day_count: int | None = Field(None, description="トライ日数")
    remarks: str | None = Field(None, description="備考")
    grade_color: str | None = Field(None, description="グレード色（カラーコード）")
    try_id: int = Field(description="トライID")


class DailyTryLog(BaseModel):
    """
    日別トライログスキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    try_date: date = Field(description="トライ日（例: 2025-04-28）")
    try_log: list[TryLogItem] = Field(description="その日のトライログ一覧")


class TryLogResponse(BaseModel):
    """
    トライログ取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    all_logs: list[DailyTryLog] = Field(description="トライログ一覧")


class YearsResponse(BaseModel):
    """
    年度取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    years: list[int] = Field(description="データが存在する年度一覧")


class MonthlyInfo(BaseModel):
    """
    月別情報スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    month: str = Field(description="月（例: 1月）")
    top_rate: float | None = Field(description="完登率（%）、データがない場合はnull")
    boulder_count: int = Field(description="挑戦課題数")
    top_count: int = Field(description="完登数")


class GradeTopRate(BaseModel):
    """
    グレード別完登率情報スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    grade: str = Field(description="グレード名（例: 3級）")
    grade_color: str = Field(description="グレード色（カラーコード）")
    monthly_info: list[MonthlyInfo] = Field(
        description="月別情報（月、上半期、下半期、年間を含む）"
    )


class TopRateResponse(BaseModel):
    """
    完登率取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    result_info: list[GradeTopRate] = Field(description="完登率情報一覧")


class AreaInfo(BaseModel):
    """
    エリア別情報スキーマ
    データがないエリアも含め、全てのエリア名を項目として返す。
    """

    model_config = ConfigDict(from_attributes=True)

    area_name: str = Field(description="エリア名（例: 強傾斜）")
    top_rate: float | None = Field(None, description="完登率（%）。データがない場合はnull")
    boulder_count: int = Field(0, description="挑戦課題数")
    top_count: int = Field(0, description="完登数")


class GradeAreaTopRate(BaseModel):
    """
    グレード別エリア完登率情報スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    grade: str = Field(description="グレード名（例: 3級）")
    grade_color: str = Field(description="グレード色（カラーコード）")
    area_info: list[AreaInfo] = Field(description="エリア別情報")


class AreaTopRateResponse(BaseModel):
    """
    エリア別完登率取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    result_info: list[GradeAreaTopRate] = Field(description="完登率情報一覧")


class BestProbItem(BaseModel):
    """
    ベスト完登課題の個別スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    prob_no: int = Field(description="課題番号", example=23)
    grade: str = Field(description="グレード名", example="3Q")
    grade_color: str = Field(description="グレード色（カラーコード）", example="FFFFFF")
    record_date: date = Field(description="記録日", example="2026-02-21")


class BestProbResponse(BaseModel):
    """
    ベスト完登課題取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    season_best: BestProbItem | None = Field(
        None, description="シーズンベスト（対象レコードがない場合はnull）"
    )
    personal_best: BestProbItem | None = Field(
        None, description="パーソナルベスト（対象レコードがない場合はnull）"
    )


class BestCountItem(BaseModel):
    """
    ベスト完登数の個別スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    grade: str = Field(description="グレード名", example="3Q")
    grade_color: str = Field(description="グレード色（カラーコード）", example="FFFFFF")
    top_count: int = Field(description="完登数", example=2)
    record_date: date = Field(description="記録日", example="2026-02-21")


class BestCountResponse(BaseModel):
    """
    ベスト完登数取得APIのレスポンススキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    season_best: BestCountItem | None = Field(
        None, description="シーズンベスト（対象レコードがない場合はnull）"
    )
    personal_best: BestCountItem | None = Field(
        None, description="パーソナルベスト（対象レコードがない場合はnull）"
    )


class TryLogEditRequest(BaseModel):
    """
    トライログ編集APIのリクエストボディスキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    try_id: int = Field(description="トライID", example=341)
    prob_no: int | None = Field(None, description="課題番号", example=3)
    result_id: int = Field(description="リザルトID", example=3)
    area_id: int | None = Field(None, description="エリアID", example=11)
    day_count: int | None = Field(None, description="トライ日数", example=1)
    remarks: str | None = Field(None, description="備考", example="青ホールド")


class TryLogRegisterItem(BaseModel):
    """
    トライログ登録リクエストの個別項目スキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    prob_no: int | None = Field(None, description="課題番号", example=3)
    grade_id: int = Field(description="グレードID", example=14)
    result_id: int = Field(description="リザルトID", example=3)
    area_id: int | None = Field(None, description="エリアID", example=11)
    day_count: int | None = Field(None, description="トライ日数", example=1)
    remarks: str | None = Field(None, description="備考")


class TryLogRegisterRequest(BaseModel):
    """
    トライログ登録APIのリクエストボディスキーマ
    """

    model_config = ConfigDict(from_attributes=True)

    gym_id: int = Field(ge=1, description="ジムID", example=1)
    try_date: date = Field(description="トライ日", example="2025-04-28")
    trylog_list: list[TryLogRegisterItem] = Field(
        min_length=1, description="トライログリスト"
    )
