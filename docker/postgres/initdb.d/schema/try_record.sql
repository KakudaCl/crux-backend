-- =====================================
-- トライ記録テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS try_record (
    "try_id" BIGSERIAL PRIMARY KEY,
    "gym_id" INTEGER NOT NULL
        REFERENCES gym_info("gym_id")
        ON DELETE CASCADE,
    "problem_number" INTEGER,
    "area_id" INTEGER
        REFERENCES area_info("area_id")
        ON DELETE CASCADE,
    "grade_id" INTEGER NOT NULL
        REFERENCES grade_info("grade_id")
        ON DELETE CASCADE,
    "result_id" INTEGER NOT NULL
        REFERENCES result_info("result_id")
        ON DELETE CASCADE,
    "try_date" DATE NOT NULL,
    "day_count" INTEGER,
    "monthly_info" VARCHAR(20)
);

COMMENT ON TABLE try_record IS 'トライ記録';
COMMENT ON COLUMN try_record."try_id" IS 'トライID';
COMMENT ON COLUMN try_record."gym_id" IS 'ジムID';
COMMENT ON COLUMN try_record."problem_number" IS '課題番号';
COMMENT ON COLUMN try_record."area_id" IS 'エリアID';
COMMENT ON COLUMN try_record."grade_id" IS 'グレードID';
COMMENT ON COLUMN try_record."result_id" IS 'トライ結果ID';
COMMENT ON COLUMN try_record."try_date" IS 'トライ日';
COMMENT ON COLUMN try_record."day_count" IS 'トライ日数';
