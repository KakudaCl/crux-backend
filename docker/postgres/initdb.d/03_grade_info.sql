-- =====================================
-- グレード情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS grade_info (
    gym_id BIGINT NOT NULL,
    grade_id BIGSERIAL,
    grade_name VARCHAR NOT NULL,
    grade_color VARCHAR(6) NOT NULL,
    CONSTRAINT grade_info_pkey PRIMARY KEY (grade_id),
    CONSTRAINT grade_info_gym_id_fkey FOREIGN KEY (gym_id)
        REFERENCES gym_info(gym_id)
        ON DELETE CASCADE,
    CONSTRAINT grade_info_grade_id_key UNIQUE (grade_id),
    CONSTRAINT grade_info_grade_name_key UNIQUE (grade_name)
);

COMMENT ON TABLE grade_info IS 'グレード情報';
COMMENT ON COLUMN grade_info.gym_id IS 'ジムID';
COMMENT ON COLUMN grade_info.grade_id IS 'グレードID';
COMMENT ON COLUMN grade_info.grade_name IS 'グレード名';
COMMENT ON COLUMN grade_info.grade_color IS 'グレード色（カラーコード）';
