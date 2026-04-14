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
    "remarks" VARCHAR(30) DEFAULT NULL,
    "is_deleted" INTEGER DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT NULL,
    "deleted_at" TIMESTAMP DEFAULT NULL
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
COMMENT ON COLUMN try_record."remarks" IS '備考';
COMMENT ON COLUMN try_record."is_deleted" IS '削除フラグ';
COMMENT ON COLUMN try_record."created_at" IS '作成日時';
COMMENT ON COLUMN try_record."updated_at" IS '更新日時';
COMMENT ON COLUMN try_record."deleted_at" IS '削除日時';