-- =====================================
-- 都道府県情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS prefecture_info (
    "prefecture_id" SERIAL PRIMARY KEY,
    "prefecture_name" VARCHAR(20) NOT NULL
);

COMMENT ON TABLE prefecture_info IS '都道府県情報';
COMMENT ON COLUMN prefecture_info."prefecture_id" IS '都道府県ID';
COMMENT ON COLUMN prefecture_info."prefecture_name" IS '都道府県名';
