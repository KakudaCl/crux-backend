-- =====================================
-- ジム情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS gym_info (
    "gym_id" SERIAL PRIMARY KEY,
    "gym_name" VARCHAR(20) NOT NULL,
    "prefecture_id" INTEGER NOT NULL
        REFERENCES prefecture_info("prefecture_id")
        ON DELETE CASCADE
);

COMMENT ON TABLE gym_info IS 'ジム情報';
COMMENT ON COLUMN gym_info."gym_id" IS 'ジムID';
COMMENT ON COLUMN gym_info."gym_name" IS 'ジム名称';
COMMENT ON COLUMN gym_info."prefecture_id" IS '都道府県ID';
