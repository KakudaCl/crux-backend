-- =====================================
-- エリア情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS area_info (
    "area_id" SERIAL PRIMARY KEY,
    "gym_id" INTEGER NOT NULL
        REFERENCES gym_info("gym_id")
        ON DELETE CASCADE,
    "area_name" VARCHAR(20) NOT NULL
);

COMMENT ON TABLE area_info IS 'エリア情報';
COMMENT ON COLUMN area_info."area_id" IS 'エリアID';
COMMENT ON COLUMN area_info."gym_id" IS 'ジムID';
COMMENT ON COLUMN area_info."area_name" IS 'エリア名';
