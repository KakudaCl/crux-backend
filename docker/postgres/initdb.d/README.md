# PostgreSQL 初期化スクリプト

このディレクトリ内のスクリプトは、PostgreSQLコンテナの**初回起動時のみ**自動的に実行されます。

## 📁 ディレクトリ構成

```
initdb.d/
├── init.sh          # 実行制御スクリプト
├── schema/             # テーブル定義（数字プレフィックスなし）
│   ├── prefecture_info.sql
│   ├── gym_info.sql
│   ├── grade_info.sql
│   ├── result_info.sql
│   ├── area_info.sql
│   └── try_record.sql
├── data/               # 初期データ
│   └── master_data.sql
└── README.md
```

## 📋 実行順序

`init.sh` スクリプトが自動的に以下の順序でSQLファイルを実行します：

### Step 1: スキーマ定義
1. **prefecture_info.sql** - 都道府県情報テーブル
2. **gym_info.sql** - ジム情報テーブル（prefecture_infoに依存）
3. **grade_info.sql** - グレード情報テーブル（gym_infoに依存）
4. **result_info.sql** - トライ結果情報テーブル
5. **area_info.sql** - エリア情報テーブル（gym_infoに依存）
6. **try_record.sql** - トライ記録テーブル（全テーブルに依存）

### Step 2: マスターデータ投入
7. **master_data.sql** - マスターデータの初期投入

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

## 📝 ファイル管理

### テーブル定義の変更方法
1. `schema/` ディレクトリ内の該当するSQLファイルを編集
2. データベースを再作成（下記の方法）

### 新しいテーブルの追加
1. `schema/` ディレクトリに新しいSQLファイルを作成（例：`user_info.sql`）
2. `init.sh` の実行順序に追加（依存関係を考慮）
3. データベースを再作成

### マスターデータの変更
1. `data/master_data.sql` を編集
2. データベースを再作成

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
**更新日**: 2026-01-28
**構成変更**: スクリプト制御方式に移行（数字プレフィックス削除）
