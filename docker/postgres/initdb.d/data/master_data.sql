-- =====================================
-- マスターデータの初期投入
-- =====================================

-- 都道府県情報の初期データ
INSERT INTO prefecture_info (prefecture_name) VALUES
    ('大阪府'), ('滋賀県'), ('東京都');

-- ジム情報の初期データ
INSERT INTO gym_info (gym_name, prefecture_id) VALUES
    ('Dボルダリングなんば', 1), ('クライミングバム大阪店', 1), ('CRUX大阪', 1),('ロックメイト大津店', 2), ('B-PUMP OGIKUBO', 3);

-- グレード情報の初期データ（一般的なボルダリンググレード）
INSERT INTO grade_info (gym_id, grade_name, grade_color) VALUES
    (2, '入門', 'DB7093'),  
    (2, '8-6級', 'FF7F00'), 
    (2, '5級', 'FFFFFF'), (2, '4級', 'FFFF00'),   
    (2, '3級', '006400'),
    (2, '2級', 'FF3D3D'),
    (3, 'VB', '1E90FF'), (3, 'V0', 'EE82EE'), (3, 'V1', 'FFFF00'), (3, 'V2', 'FF0000'), (3, 'V3', '622D18'), (3, 'V4', 'A0A0A0');

-- トライ結果情報の初期データ
INSERT INTO result_info (result_name) VALUES
    ('FLASH'),    -- 一撃でクリア
    ('TOP'),      -- 完登
    ('ZONE'),     -- ゾーンまで到達
    ('NOSCORE')   -- スコアなし（トライのみ）
;

-- エリア情報の初期データ（一般的な壁の種類）
INSERT INTO area_info (gym_id, area_name) VALUES
    (2, 'A-Wall'),        
    (2, 'B-Wall'),      
    (2, 'C-Wall'),
    (2, 'D-Wall'),    
    (2, 'E-Wall'),     
    (2, 'F-Wall'),     
    (3, 'スラブ'),
    (3, '垂壁'),
    (3, 'うすかぶり'),
    (3, '強傾斜'),
    (3, 'シップウォール'),
    (3, 'シップルーフ');

-- 初期データ投入完了メッセージ
DO $$
BEGIN
    RAISE NOTICE '✅ マスターデータの初期化が完了しました';
    RAISE NOTICE '   - 都道府県: % 件', (SELECT COUNT(*) FROM prefecture_info);
    RAISE NOTICE '   - グレード: % 件', (SELECT COUNT(*) FROM grade_info);
    RAISE NOTICE '   - 結果情報: % 件', (SELECT COUNT(*) FROM result_info);
    RAISE NOTICE '   - エリア情報: % 件', (SELECT COUNT(*) FROM area_info);
END $$;
