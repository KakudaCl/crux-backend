-- =====================================
-- トライ記録テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS try_record (
    "try_id" BIGSERIAL PRIMARY KEY,
    "gym_id" INTEGER NOT NULL
        REFERENCES gym_info("gym_id")
        ON DELETE CASCADE,
    "problem_number" INTEGER DEFAULT NULL,
    "area_id" INTEGER DEFAULT NULL
        REFERENCES area_info("area_id")
        ON DELETE CASCADE,
    "grade_id" INTEGER NOT NULL
        REFERENCES grade_info("grade_id")
        ON DELETE CASCADE,
    "result_id" INTEGER NOT NULL
        REFERENCES result_info("result_id")
        ON DELETE CASCADE,
    "try_date" DATE DEFAULT NULL,
    "day_count" INTEGER DEFAULT NULL,
    "monthly_info" VARCHAR(20) DEFAULT NULL,
    "remarks" VARCHAR(30) DEFAULT NULL,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION set_try_record_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW."updated_at" := DATE_TRUNC('second', CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_try_record_updated_at
BEFORE UPDATE ON try_record
FOR EACH ROW
EXECUTE FUNCTION set_try_record_updated_at();

COMMENT ON TABLE try_record IS 'トライ記録';
COMMENT ON COLUMN try_record."try_id" IS 'トライID';
COMMENT ON COLUMN try_record."gym_id" IS 'ジムID';
COMMENT ON COLUMN try_record."problem_number" IS '課題番号';
COMMENT ON COLUMN try_record."area_id" IS 'エリアID';
COMMENT ON COLUMN try_record."grade_id" IS 'グレードID';
COMMENT ON COLUMN try_record."result_id" IS 'トライ結果ID';
COMMENT ON COLUMN try_record."try_date" IS 'トライ日';
COMMENT ON COLUMN try_record."day_count" IS 'トライ日数';
COMMENT ON COLUMN try_record."monthly_info" IS 'マンスリー情報';
COMMENT ON COLUMN try_record."remarks" IS '備考';
COMMENT ON COLUMN try_record."created_at" IS '作成日時';
COMMENT ON COLUMN try_record."updated_at" IS '更新日時';