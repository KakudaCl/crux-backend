-- =====================================
-- トライ記録テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS try_record (
    try_id BIGSERIAL,
    gym_id INTEGER NOT NULL,
    grade_id INTEGER NOT NULL,
    problem_number INTEGER NOT NULL,
    area_id INTEGER,
    result_id INTEGER NOT NULL,
    try_date TIMESTAMP NOT NULL,
    day_count INTEGER,
    CONSTRAINT try_record_pkey PRIMARY KEY (try_id),
    CONSTRAINT try_record_gym_id_fkey FOREIGN KEY (gym_id)
        REFERENCES gym_info(gym_id)
        ON DELETE CASCADE,
    CONSTRAINT try_record_grade_id_fkey FOREIGN KEY (grade_id)
        REFERENCES grade_info(grade_id)
        ON DELETE CASCADE,
    CONSTRAINT try_record_area_id_fkey FOREIGN KEY (area_id)
        REFERENCES area_info(area_id)
        ON DELETE SET NULL,
    CONSTRAINT try_record_result_id_fkey FOREIGN KEY (result_id)
        REFERENCES result_info(result_id)
        ON DELETE CASCADE
);

-- インデックスの作成（パフォーマンス向上のため）
CREATE INDEX IF NOT EXISTS ix_try_record_gym_id ON try_record(gym_id);
CREATE INDEX IF NOT EXISTS ix_try_record_grade_id ON try_record(grade_id);
CREATE INDEX IF NOT EXISTS ix_try_record_result_id ON try_record(result_id);
CREATE INDEX IF NOT EXISTS ix_try_record_area_id ON try_record(area_id);
CREATE INDEX IF NOT EXISTS ix_try_record_try_date ON try_record(try_date);

COMMENT ON TABLE try_record IS 'トライ記録';
COMMENT ON COLUMN try_record.try_id IS 'トライID';
COMMENT ON COLUMN try_record.gym_id IS 'ジムID';
COMMENT ON COLUMN try_record.grade_id IS 'グレードID';
COMMENT ON COLUMN try_record.problem_number IS '課題番号';
COMMENT ON COLUMN try_record.area_id IS 'エリアID';
COMMENT ON COLUMN try_record.result_id IS 'トライ結果ID';
COMMENT ON COLUMN try_record.try_date IS 'トライ日';
COMMENT ON COLUMN try_record.day_count IS 'トライ日数';
