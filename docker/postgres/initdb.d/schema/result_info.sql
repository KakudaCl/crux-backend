-- =====================================
-- トライ結果情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS result_info (
    "result_id" SERIAL PRIMARY KEY,
    "result_name" VARCHAR(10) NOT NULL
);

COMMENT ON TABLE result_info IS 'トライ結果情報';
COMMENT ON COLUMN result_info."result_id" IS 'トライ結果ID';
COMMENT ON COLUMN result_info."result_name" IS 'トライ結果名（FLASH/TOP/ZONE/NOSCORE）';
