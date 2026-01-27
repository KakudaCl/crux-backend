-- =====================================
-- マスターデータの初期投入
-- =====================================

-- 都道府県情報の初期データ
INSERT INTO prefecture_info (prefecture_name) VALUES
    ('北海道'), ('青森県'), ('岩手県'), ('宮城県'), ('秋田県'),
    ('山形県'), ('福島県'), ('茨城県'), ('栃木県'), ('群馬県'),
    ('埼玉県'), ('千葉県'), ('東京都'), ('神奈川県'), ('新潟県'),
    ('富山県'), ('石川県'), ('福井県'), ('山梨県'), ('長野県'),
    ('岐阜県'), ('静岡県'), ('愛知県'), ('三重県'), ('滋賀県'),
    ('京都府'), ('大阪府'), ('兵庫県'), ('奈良県'), ('和歌山県'),
    ('鳥取県'), ('島根県'), ('岡山県'), ('広島県'), ('山口県'),
    ('徳島県'), ('香川県'), ('愛媛県'), ('高知県'), ('福岡県'),
    ('佐賀県'), ('長崎県'), ('熊本県'), ('大分県'), ('宮崎県'),
    ('鹿児島県'), ('沖縄県')
ON CONFLICT (prefecture_name) DO NOTHING;

-- グレード情報の初期データ（一般的なボルダリンググレード）
INSERT INTO grade_info (grade_name, grade_color) VALUES
    ('10級', 'FFFFFF'),  -- 白
    ('9級', 'FFFF00'),   -- 黄色
    ('8級', 'FFA500'),   -- オレンジ
    ('7級', 'FF69B4'),   -- ピンク
    ('6級', '00FF00'),   -- 緑
    ('5級', '0000FF'),   -- 青
    ('4級', '800080'),   -- 紫
    ('3級', '8B4513'),   -- 茶色
    ('2級', '000000'),   -- 黒
    ('1級', 'C0C0C0'),   -- 銀
    ('初段', 'FFD700'),  -- 金
    ('二段', 'FFD700'),
    ('三段', 'FFD700'),
    ('四段', 'FFD700'),
    ('五段', 'FFD700')
ON CONFLICT (grade_name) DO NOTHING;

-- トライ結果情報の初期データ
INSERT INTO result_info (result_name) VALUES
    ('FLASH'),    -- 一撃でクリア
    ('TOP'),      -- 完登
    ('ZONE'),     -- ゾーンまで到達
    ('NOSCORE')   -- スコアなし（トライのみ）
ON CONFLICT DO NOTHING;

-- エリア情報の初期データ（一般的な壁の種類）
INSERT INTO area_info (area_name) VALUES
    ('垂壁'),        -- 垂直な壁
    ('スラブ'),      -- 傾斜が緩い壁
    ('薄かぶり'),    -- 少し傾斜
    ('かぶり壁'),    -- 傾斜がきつい壁
    ('強傾斜'),      -- 非常に傾斜
    ('ルーフ'),      -- 天井
    ('その他')
ON CONFLICT (area_name) DO NOTHING;

-- 初期データ投入完了メッセージ
DO $$
BEGIN
    RAISE NOTICE '✅ マスターデータの初期化が完了しました';
    RAISE NOTICE '   - 都道府県: % 件', (SELECT COUNT(*) FROM prefecture_info);
    RAISE NOTICE '   - グレード: % 件', (SELECT COUNT(*) FROM grade_info);
    RAISE NOTICE '   - 結果情報: % 件', (SELECT COUNT(*) FROM result_info);
    RAISE NOTICE '   - エリア情報: % 件', (SELECT COUNT(*) FROM area_info);
END $$;
