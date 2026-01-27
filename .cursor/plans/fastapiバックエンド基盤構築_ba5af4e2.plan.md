---
name: FastAPIバックエンド基盤構築
overview: FastAPI + SQLAlchemy + PostgreSQLを使用したボルダリング記録アプリケーションのバックエンドプロジェクトの叩き台を作成し、テーブル定義書に基づいた6つのテーブルモデルを実装いたしますわ。
todos:
  - id: setup-structure
    content: プロジェクトディレクトリ構造とパッケージファイルの作成
    status: completed
  - id: setup-dependencies
    content: requirements.txt、.gitignore、.env.exampleの作成
    status: completed
    dependencies:
      - setup-structure
  - id: implement-config
    content: 設定管理（config.py）とデータベース接続（database.py）の実装
    status: completed
    dependencies:
      - setup-dependencies
  - id: implement-models
    content: 6つのテーブルモデルの実装（依存順序に従って）
    status: completed
    dependencies:
      - implement-config
  - id: setup-alembic
    content: Alembicのセットアップと初期マイグレーションの作成
    status: completed
    dependencies:
      - implement-models
  - id: implement-main
    content: FastAPIアプリケーション（main.py）の実装
    status: completed
    dependencies:
      - implement-models
  - id: update-readme
    content: READMEの更新とセットアップドキュメントの作成
    status: completed
    dependencies:
      - setup-alembic
      - implement-main
---

# FastAPIバックエンドプロジェクト構築プラン

## 1. プロジェクト構造の作成

標準的なFastAPIプロジェクト構造を作成いたしますわ：

```
crux-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPIアプリケーションのエントリーポイント
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 設定管理（環境変数など）
│   │   └── database.py        # データベース接続設定
│   ├── models/
│   │   ├── __init__.py
│   │   ├── try_record.py      # トライ記録モデル
│   │   ├── gym_info.py        # ジム情報モデル
│   │   ├── prefecture_info.py # 都道府県情報モデル
│   │   ├── grade_info.py      # グレード情報モデル
│   │   ├── result_info.py     # トライ結果情報モデル
│   │   └── area_info.py       # エリア情報モデル
│   └── api/                   # API実装用（将来的に使用）
│       └── __init__.py
├── alembic/                   # マイグレーション管理
│   └── versions/
├── requirements.txt           # 依存パッケージ
├── .env.example              # 環境変数のサンプル
├── .gitignore                # Git除外設定
└── alembic.ini               # Alembicの設定ファイル
```

## 2. 依存パッケージの定義

[requirements.txt](requirements.txt)を作成し、以下のパッケージを含めますわ：

- fastapi
- uvicorn[standard]
- sqlalchemy
- psycopg2-binary
- alembic
- python-dotenv
- pydantic-settings

## 3. データベース接続設定

### 3.1 設定管理

[app/core/config.py](app/core/config.py)にて、Pydantic Settingsを使用して環境変数から設定を読み込みますわ：

- DATABASE_URL
- その他の環境設定

### 3.2 データベースセッション管理

[app/core/database.py](app/core/database.py)にて：

- SQLAlchemyのengineとsessionmakerを設定
- Baseクラスの定義（全モデルの基底クラス）
- データベース接続の依存性注入用関数

## 4. テーブルモデルの実装

テーブル仕様書に基づいて、6つのSQLAlchemyモデルを作成いたしますわ：

### 4.1 prefecture_info（都道府県情報）

最も依存関係の少ないテーブルから実装：

- prefecture_id: BigInteger, PK, Auto increment
- prefecture_name: String(20), Not Null

### 4.2 gym_info（ジム情報）

prefecture_infoを参照：

- gym_id: BigInteger, PK, Auto increment
- gym_name: String(20), Not Null
- prefecture_id: BigInteger, FK → prefecture_info

### 4.3 grade_info（グレード情報）

- grade_id: BigInteger, PK, UK, Auto increment
- grade_name: String, Not Null, UK
- grade_color: String(6), Not Null（カラーコード）

### 4.4 result_info（トライ結果情報）

- result_id: BigInteger, PK, Auto increment
- result_name: String(10), Not Null（FLASH/TOP/ZONE/NOSCOREなど）

### 4.5 area_info（エリア情報）

- area_id: BigInteger, PK, UK, Auto increment
- area_name: String(10), Not Null, UK

### 4.6 try_record（トライ記録）

全テーブルを参照するメインテーブル：

- try_id: BigInteger, PK, Auto increment
- gym_id: BigInteger, FK → gym_info, Not Null
- grade_id: BigInteger, FK → grade_info, Not Null
- problem_number: Integer, Not Null
- area_id: BigInteger, FK → area_info, Nullable
- result_id: BigInteger, FK → result_info, Not Null
- try_date: DateTime, Not Null
- day_count: Integer, Nullable

各モデルには：

- `__tablename__`属性
- リレーションシップの定義
- `__repr__`メソッド

## 5. Alembicマイグレーションのセットアップ

### 5.1 Alembicの初期化

- `alembic init alembic`相当の設定
- [alembic.ini](alembic.ini)の作成
- [alembic/env.py](alembic/env.py)にてBaseのメタデータをインポート

### 5.2 初期マイグレーションの作成

全テーブルを作成する初回マイグレーションファイルを生成

## 6. FastAPIアプリケーションの基本セットアップ

[app/main.py](app/main.py)にて：

- FastAPIインスタンスの作成
- CORSミドルウェアの設定
- ヘルスチェックエンドポイント（`GET /health`）
- 起動時のデータベース接続確認

## 7. 環境設定ファイル

### 7.1 .env.example

環境変数のサンプルファイル：

```
DATABASE_URL=postgresql://user:password@localhost:5432/crux_db
```

### 7.2 .gitignore

Python/FastAPI向けの適切な除外設定

## 8. README更新

基本的なセットアップ手順を含む[README.md](README.md)の更新：

- プロジェクト概要
- セットアップ手順
- データベースマイグレーション手順
- 起動方法

## 実装の順序

1. ✅ プロジェクト構造の作成
2. ✅ requirements.txtの作成
3. ✅ .gitignoreと.env.exampleの作成
4. ✅ 設定管理（config.py）の実装
5. ✅ データベース接続（database.py）の実装
6. ✅ モデルの実装（依存関係の順序で）
7. ✅ Alembicのセットアップ
8. ✅ FastAPIアプリケーション（main.py）の実装
9. ✅ READMEの更新

## テーブル間の関係図

```mermaid
erDiagram
    prefecture_info ||--o{ gym_info : "都道府県"
    gym_info ||--o{ try_record : "ジム"
    grade_info ||--o{ try_record : "グレード"
    result_info ||--o{ try_record : "結果"
    area_info ||--o| try_record : "エリア"
    
    prefecture_info {
        bigint prefecture_id PK
        varchar prefecture_name UK
    }
    
    gym_info {
        bigint gym_id PK
        varchar gym_name
        bigint prefecture_id FK
    }
    
    grade_info {
        bigint grade_id PK
        varchar grade_name UK
        varchar grade_color
    }
    
    result_info {
        bigint result_id PK
        varchar result_name
    }
    
    area_info {
        bigint area_id PK
        varchar area_name UK
    }
    
    try_record {
        bigint try_id PK
        bigint gym_id FK
        bigint grade_id FK
        int problem_number
        bigint area_id FK
        bigint result_id FK
        datetime try_date
        int day_count
    }
```

## 注意事項

- API実装は含めません（今回は叩き台のみ）
- テーブル定義とデータベース接続の基盤構築に焦点を当てますわ
- マイグレーションファイルは自動生成ではなく、手動で確実に作成いたしますわ