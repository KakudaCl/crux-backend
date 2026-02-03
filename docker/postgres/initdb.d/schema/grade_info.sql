-- =====================================
-- グレード情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS grade_info (
    "grade_id" SERIAL PRIMARY KEY,
    "gym_id" INTEGER NOT NULL
        REFERENCES gym_info("gym_id")
        ON DELETE CASCADE,
    "grade_name" VARCHAR(10) NOT NULL,
    "grade_color" VARCHAR(6) NOT NULL
);

COMMENT ON TABLE grade_info IS 'グレード情報';
COMMENT ON COLUMN grade_info."grade_id" IS 'グレードID';
COMMENT ON COLUMN grade_info."gym_id" IS 'ジムID';
COMMENT ON COLUMN grade_info."grade_name" IS 'グレード名';
COMMENT ON COLUMN grade_info."grade_color" IS 'グレード色（カラーコード）';
