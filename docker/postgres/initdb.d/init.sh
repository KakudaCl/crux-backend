#!/bin/bash
# =====================================
# PostgreSQL 初期化スクリプト
# 実行順序を制御してSQLファイルを読み込む
# =====================================

set -e  # エラーが発生したら即座に終了

# 色付きログ用の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}🚀 データベース初期化を開始します${NC}"
echo -e "${BLUE}=========================================${NC}"

# ベースパス
BASE_PATH="/docker-entrypoint-initdb.d"

# スキーマ定義を順番に実行
echo -e "${GREEN}📋 Step 1: スキーマ定義を作成中...${NC}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	\echo '  → prefecture_info テーブルを作成'
	\i ${BASE_PATH}/schema/prefecture_info.sql
	
	\echo '  → gym_info テーブルを作成'
	\i ${BASE_PATH}/schema/gym_info.sql
	
	\echo '  → grade_info テーブルを作成'
	\i ${BASE_PATH}/schema/grade_info.sql
	
	\echo '  → result_info テーブルを作成'
	\i ${BASE_PATH}/schema/result_info.sql
	
	\echo '  → area_info テーブルを作成'
	\i ${BASE_PATH}/schema/area_info.sql
	
	\echo '  → try_record テーブルを作成'
	\i ${BASE_PATH}/schema/try_record.sql
EOSQL

echo -e "${GREEN}✅ スキーマ定義が完了しました${NC}"
echo ""

# マスターデータを投入
echo -e "${GREEN}📦 Step 2: マスターデータを投入中...${NC}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	\i ${BASE_PATH}/data/master_data.sql
EOSQL

echo -e "${GREEN}✅ マスターデータの投入が完了しました${NC}"
echo ""

# 完了メッセージ
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}🎉 データベース初期化が完了しました！${NC}"
echo -e "${BLUE}=========================================${NC}"
