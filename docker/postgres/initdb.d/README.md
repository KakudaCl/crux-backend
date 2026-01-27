# PostgreSQL 初期化スクリプト

このディレクトリ内のSQLファイルは、PostgreSQLコンテナの**初回起動時のみ**自動的に実行されます。

## 📋 実行順序

ファイルはアルファベット順（番号順）に実行されます：

1. **01_prefecture_info.sql** - 都道府県情報テーブル
2. **02_gym_info.sql** - ジム情報テーブル（prefecture_infoに依存）
3. **03_grade_info.sql** - グレード情報テーブル
4. **04_result_info.sql** - トライ結果情報テーブル
5. **05_area_info.sql** - エリア情報テーブル
6. **06_try_record.sql** - トライ記録テーブル（全テーブルに依存）
7. **10_master_data.sql** - マスターデータの初期投入

## ⚠️ 重要な注意事項

### 初回起動時のみ実行

- このディレクトリのスクリプトは、**データボリュームが空の状態での初回起動時のみ**実行されます
- 2回目以降の起動では実行されません

### スクリプトを再実行する方法

```bash
# データベースとボリュームを削除
docker-compose down -v

# 再起動（スクリプトが再度実行される）
docker-compose up -d
```

## 📝 ファイル命名規則

- **01-09**: テーブル定義（依存関係の順序）
- **10-19**: 初期データ投入
- **20-29**: インデックス作成（将来用）
- **30-39**: ビュー作成（将来用）

## ✏️ テーブル定義の変更方法

1. 該当するSQLファイルを編集
2. データベースを再作成（上記の方法）

## ➕ 新しいテーブルの追加

1. 新しいSQLファイルを作成（例：`07_new_table.sql`）
2. 依存関係を考慮して番号を決定
3. データベースを再作成

## 🔍 実行ログの確認

```bash
# PostgreSQLコンテナのログを確認
docker-compose logs postgres

# 初期化スクリプトの実行結果が表示されます
```

## 📊 テーブル構造の確認

```bash
# PostgreSQLに接続
docker-compose exec postgres psql -U crux_user -d crux_db

# テーブル一覧
\dt

# 特定のテーブル構造を確認
\d prefecture_info
\d gym_info
\d try_record

# 終了
\q
```

## 🔗 テーブル関係図

```
prefecture_info (都道府県)
    ↓ 1:N
gym_info (ジム)
    ↓ 1:N
try_record (トライ記録) ← grade_info (グレード)
    ↑                    ← result_info (結果)
    └── 0:1 ───────────  area_info (エリア)
```

---

**作成日**: 2026-01-27
**更新日**: 2026-01-27
