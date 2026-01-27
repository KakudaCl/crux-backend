-- =====================================
-- エリア情報テーブル
-- =====================================

CREATE TABLE IF NOT EXISTS area_info (
    area_id BIGSERIAL,
    area_name VARCHAR(10) NOT NULL,
    CONSTRAINT area_info_pkey PRIMARY KEY (area_id),
    CONSTRAINT area_info_area_id_key UNIQUE (area_id),
    CONSTRAINT area_info_area_name_key UNIQUE (area_name)
);

COMMENT ON TABLE area_info IS 'エリア情報';
COMMENT ON COLUMN area_info.area_id IS 'エリアID';
COMMENT ON COLUMN area_info.area_name IS 'エリア名';
