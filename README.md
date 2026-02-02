# CRUX Backend

ボルダリングのトライ記録を管理するFastAPIバックエンドアプリケーション

## 📋 プロジェクト概要

CRUX Backendは、ボルダリングジムでの挑戦結果を記録・管理するためのREST APIを提供するバックエンドシステムです。

### 主な機能

- トライ記録の管理
- ジム情報の管理
- グレード情報の管理
- 都道府県情報の管理
- トライ結果の管理
- エリア情報の管理

## 🛠 技術スタック

- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0.25
- **DB Migration**: SQL Scripts (docker-entrypoint-initdb.d)
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## 📦 プロジェクト構造

```
crux-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPIアプリケーションのエントリーポイント
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 設定管理（環境変数など）
│   │   └── database.py        # データベース接続設定
│   ├── models/                # SQLAlchemyモデル
│   │   ├── __init__.py
│   │   ├── try_record.py      # トライ記録モデル
│   │   ├── gym_info.py        # ジム情報モデル
│   │   ├── prefecture_info.py # 都道府県情報モデル
│   │   ├── grade_info.py      # グレード情報モデル
│   │   ├── result_info.py     # トライ結果情報モデル
│   │   └── area_info.py       # エリア情報モデル
│   └── api/                   # API実装用（将来的に使用）
│       └── __init__.py
├── docker/                    # Docker関連ファイル
│   └── postgres/
│       └── initdb.d/          # PostgreSQL初期化スクリプト
│           ├── 01_prefecture_info.sql
│           ├── 02_gym_info.sql
│           ├── 03_grade_info.sql
│           ├── 04_result_info.sql
│           ├── 05_area_info.sql
│           ├── 06_try_record.sql
│           └── 10_master_data.sql
├── requirements.txt           # 依存パッケージ
├── .env.example              # 環境変数のサンプル（ローカル開発用）
├── .env.docker.example       # 環境変数のサンプル（Docker用）
├── .gitignore                # Git除外設定
├── .dockerignore             # Docker除外設定
├── Dockerfile                # Docker イメージ定義
├── docker-compose.yml        # Docker Compose 設定
└── README.md                 # このファイル
```

## 🚀 セットアップ

### 🐳 Docker を使用する場合（推奨）

Dockerを使用すると、PostgreSQLとFastAPIアプリケーションを簡単に起動できます。

#### 前提条件

- Docker
- Docker Compose

#### クイックスタート

```bash
# 1. リポジトリのクローン
git clone <repository-url>
cd crux-backend

# 2. 環境変数の設定（オプション）
cp .env.docker.example .env
# 必要に応じて .env ファイルを編集

# 3. Docker Compose でアプリケーションを起動
docker-compose up -d

# 4. ログの確認
docker-compose logs -f api

# 5. アプリケーションへアクセス
# http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

#### Docker コマンド

```bash
# コンテナの起動
docker-compose up -d

# ログの確認
docker-compose logs -f         # 全てのサービス
docker-compose logs -f api     # APIのみ
docker-compose logs -f postgres # PostgreSQLのみ

# コンテナの停止
docker-compose down

# コンテナとボリュームの削除（データベースデータも削除）
docker-compose down -v

# コンテナの再構築
docker-compose up -d --build

# コンテナ内でコマンド実行
docker-compose exec api bash                                # API コンテナに入る
docker-compose exec postgres psql -U crux_user -d crux_db  # PostgreSQLに接続
```

---

### 💻 ローカル環境で直接実行する場合

#### 前提条件

- Python 3.11以上
- PostgreSQL 14以上
- pip

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd crux-backend
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成し、必要な設定を記入します。

```bash
cp .env.example .env
```

`.env`ファイルの編集:

```env
# Database Configuration
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/crux_db

# Application Configuration
APP_NAME="CRUX Backend API"
APP_VERSION="0.1.0"
DEBUG=True

# API Configuration
API_V1_PREFIX="/api/v1"
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### 5. データベースの準備

PostgreSQLデータベースを作成します。

```bash
# PostgreSQLにログイン
psql -U postgres

# データベースとユーザーの作成
CREATE DATABASE crux_db;
CREATE USER crux_user WITH PASSWORD 'crux_password';
GRANT ALL PRIVILEGES ON DATABASE crux_db TO crux_user;
\q
```

### 6. データベースの初期化

PostgreSQLコンテナの初回起動時に、`docker/postgres/initdb.d/` 内のSQLファイルが自動的に実行され、
テーブルとマスターデータが作成されます。

特別な操作は不要です。

### 7. アプリケーションの起動

```bash
# 開発サーバーの起動
python -m app.main

# または uvicorn を直接使用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

アプリケーションは `http://localhost:8000` で起動します。

## 📚 API ドキュメント

FastAPIは自動的にAPIドキュメントを生成します。

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 エンドポイント

### ヘルスチェック

```bash
# ルートエンドポイント
GET http://localhost:8000/

# ヘルスチェック（データベース接続確認）
GET http://localhost:8000/health
```

### 完登率取得API

年度/ジム/グレード別の完登率情報を取得します。

**エンドポイント**: `GET /api/v1/top_rates`

**クエリパラメータ**:
- `year` (integer, 必須): 年度（例: 2026）
- `gym_id` (integer, 必須): ジムID（例: 1）

**レスポンス例**:

```json
{
  "result_info": [
    {
      "grade": "3級",
      "monthly_info": [
        {
          "month": "1月",
          "top_rate": 50.0,
          "boulder_count": 24,
          "top_count": 12
        },
        {
          "month": "2月",
          "top_rate": 75.5,
          "boulder_count": 20,
          "top_count": 15
        }
      ]
    }
  ]
}
```

**使用例**:

```bash
# cURLでのリクエスト
curl "http://localhost:8000/api/v1/top_rates?year=2026&gym_id=1"

# httpieでのリクエスト（より見やすい）
http GET "http://localhost:8000/api/v1/top_rates" year==2026 gym_id==1
```

**レスポンスフィールド**:
- `result_info`: グレード別の完登率情報配列
  - `grade`: グレード名（例: "3級"）
  - `monthly_info`: 月別情報配列
    - `month`: 月（例: "1月"）
    - `top_rate`: 完登率（%、小数第2位まで）
    - `boulder_count`: 挑戦課題数
    - `top_count`: 完登数（FLASHまたはTOPの結果）

**エラーレスポンス**:
- `400 Bad Request`: パラメータが不正な場合
- `500 Internal Server Error`: サーバー内部エラー

## 🗄 データベーススキーマ

### テーブル一覧

1. **prefecture_info** - 都道府県情報
2. **gym_info** - ジム情報
3. **grade_info** - グレード情報
4. **result_info** - トライ結果情報
5. **area_info** - エリア情報
6. **try_record** - トライ記録（メインテーブル）

### テーブル関係図

```
prefecture_info (都道府県情報)
    ↓ 1:N
gym_info (ジム情報)
    ↓ 1:N
try_record (トライ記録) ← grade_info (グレード情報)
    ↑                    ← result_info (トライ結果情報)
    └─ 0:N ──────────── area_info (エリア情報)
```

詳細なテーブル定義は `テーブル仕様書.xlsx` を参照してください。

## 🔧 開発

### Docker環境での開発

Docker Composeを使用すると、開発環境を素早く構築できます。

```bash
# 開発サーバーの起動（ホットリロード有効）
docker-compose up -d

# コードを変更すると自動的に再読み込みされます
# app/ディレクトリがマウントされています

# APIコンテナのシェルに入る
docker-compose exec api bash

# コンテナ内でPythonシェルを起動
docker-compose exec api python

# データベースに直接接続
docker-compose exec postgres psql -U crux_user -d crux_db
```

### データベーススキーマの管理

テーブル定義は `docker/postgres/initdb.d/` ディレクトリのSQLファイルで管理されています。

#### テーブル定義の変更方法

1. 該当するSQLファイル（例：`01_prefecture_info.sql`）を編集
2. データベースを再作成

```bash
# データベースとボリュームを削除
docker-compose down -v

# 再起動（SQLファイルが自動実行される）
docker-compose up -d
```

#### 新しいテーブルの追加

1. `docker/postgres/initdb.d/` に新しいSQLファイルを作成
   - ファイル名は `07_テーブル名.sql` のように番号付き
   - 依存関係を考慮して番号を付ける
2. データベースを再作成（上記手順）

#### マスターデータの変更

`docker/postgres/initdb.d/10_master_data.sql` を編集して、データベースを再作成します。

### コードフォーマット

```bash
# Black によるフォーマット（推奨）
pip install black
black app/

# isort によるインポート整理（推奨）
pip install isort
isort app/
```

### リンター

```bash
# flake8 によるコードチェック（推奨）
pip install flake8
flake8 app/

# mypy による型チェック（推奨）
pip install mypy
mypy app/
```

## 📝 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `DATABASE_URL` | PostgreSQL接続URL | `postgresql://crux_user:crux_password@localhost:5432/crux_db` |
| `APP_NAME` | アプリケーション名 | `"CRUX Backend API"` |
| `APP_VERSION` | アプリケーションバージョン | `"0.1.0"` |
| `DEBUG` | デバッグモード | `True` |
| `API_V1_PREFIX` | API v1のプレフィックス | `"/api/v1"` |
| `ALLOWED_ORIGINS` | CORS許可オリジン | `["http://localhost:3000", "http://localhost:8080"]` |

## 🧪 テスト

```bash
# テストの実行（将来的に実装）
pytest

# カバレッジ付きテスト
pytest --cov=app tests/
```

## 📄 ライセンス

このプロジェクトは内部使用のみを目的としています。

## 👥 開発者

CRUX Development Team

## 📞 サポート

問題が発生した場合は、Issue を作成してください。

---

**Version**: 0.1.0  
**Last Updated**: 2026-01-27
