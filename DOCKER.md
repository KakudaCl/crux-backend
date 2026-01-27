# Docker 使用ガイド

CRUX BackendをDockerで実行するための詳細ガイドです。

## 📋 目次

- [前提条件](#前提条件)
- [クイックスタート](#クイックスタート)
- [環境変数の設定](#環境変数の設定)
- [よく使うコマンド](#よく使うコマンド)
- [開発時の Tips](#開発時の-tips)
- [トラブルシューティング](#トラブルシューティング)

## 前提条件

以下がインストールされている必要があります：

- **Docker**: 20.10.0 以上
- **Docker Compose**: 2.0.0 以上

### インストール確認

```bash
docker --version
docker-compose --version
```

## クイックスタート

### 1. 環境変数の設定（オプション）

デフォルト設定で問題なければスキップ可能です。

```bash
# Docker用の環境変数ファイルを作成
cp .env.docker.example .env

# 必要に応じて編集
vim .env
```

### 2. アプリケーションの起動

```bash
# バックグラウンドで起動
docker-compose up -d

# ログを表示しながら起動
docker-compose up
```

### 3. 起動確認

```bash
# コンテナの状態確認
docker-compose ps

# ログの確認
docker-compose logs -f

# ヘルスチェック
curl http://localhost:8000/health
```

### 4. API ドキュメントへアクセス

ブラウザで以下のURLにアクセス：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **ルート**: http://localhost:8000/

## 環境変数の設定

`.env` ファイルで以下の変数を設定できます：

### データベース設定

```env
POSTGRES_USER=crux_user          # PostgreSQLのユーザー名
POSTGRES_PASSWORD=crux_password  # PostgreSQLのパスワード
POSTGRES_DB=crux_db              # データベース名
POSTGRES_PORT=5432               # PostgreSQLのポート（ホスト側）
```

### API設定

```env
API_PORT=8000                    # APIのポート（ホスト側）
APP_NAME="CRUX Backend API"     # アプリケーション名
APP_VERSION="0.1.0"             # バージョン
DEBUG=True                       # デバッグモード
```

### CORS設定

```env
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## よく使うコマンド

### コンテナの管理

```bash
# コンテナの起動
docker-compose up -d

# コンテナの停止
docker-compose stop

# コンテナの停止と削除
docker-compose down

# コンテナとボリュームの削除（データベースデータも削除）
docker-compose down -v

# コンテナの再起動
docker-compose restart

# 特定のサービスのみ再起動
docker-compose restart api
docker-compose restart postgres
```

### ログの確認

```bash
# 全サービスのログを表示
docker-compose logs

# リアルタイムでログを表示
docker-compose logs -f

# 特定のサービスのログのみ表示
docker-compose logs -f api
docker-compose logs -f postgres

# 最新100行のみ表示
docker-compose logs --tail=100 api
```

### コンテナ内でのコマンド実行

```bash
# APIコンテナのシェルに入る
docker-compose exec api bash

# PostgreSQLコンテナのシェルに入る
docker-compose exec postgres bash

# PostgreSQLに接続
docker-compose exec postgres psql -U crux_user -d crux_db

# Pythonシェルを起動
docker-compose exec api python

# 特定のコマンドを実行
docker-compose exec api alembic current
```

### データベースマイグレーション

```bash
# マイグレーション状態の確認
docker-compose exec api alembic current

# マイグレーション履歴の確認
docker-compose exec api alembic history

# マイグレーションの適用
docker-compose exec api alembic upgrade head

# マイグレーションのロールバック
docker-compose exec api alembic downgrade -1

# 新しいマイグレーションの作成
docker-compose exec api alembic revision --autogenerate -m "description"
```

### イメージの管理

```bash
# イメージの再ビルド
docker-compose build

# キャッシュを使わずにビルド
docker-compose build --no-cache

# ビルドして起動
docker-compose up -d --build

# 使用していないイメージの削除
docker image prune

# 全ての停止中のコンテナ、未使用のネットワーク、イメージを削除
docker system prune
```

### データベース操作

```bash
# データベースのバックアップ
docker-compose exec postgres pg_dump -U crux_user crux_db > backup.sql

# バックアップからリストア
docker-compose exec -T postgres psql -U crux_user crux_db < backup.sql

# データベースをリセット
docker-compose down -v
docker-compose up -d
```

## 開発時の Tips

### ホットリロード

`docker-compose.yml` では `app/` と `alembic/` ディレクトリをマウントしているため、
コードを変更すると自動的にアプリケーションが再読み込みされます。

### デバッグ

```bash
# APIコンテナのログをリアルタイムで表示
docker-compose logs -f api

# コンテナ内でインタラクティブにPythonを実行
docker-compose exec api python
>>> from app.core.database import SessionLocal
>>> db = SessionLocal()
>>> # デバッグコードをここに書く
```

### コンテナ内での開発

```bash
# コンテナ内に入る
docker-compose exec api bash

# 中で作業
cd /app
ls -la
python -m pytest
```

### 環境のリセット

開発中にデータベースをクリーンな状態に戻したい場合：

```bash
# 全てを停止してボリュームも削除
docker-compose down -v

# 再起動（マイグレーションが自動実行される）
docker-compose up -d

# ログを確認
docker-compose logs -f api
```

## トラブルシューティング

### ポートが既に使用されている

```bash
# エラー: Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use

# 解決方法1: 別のポートを使用
# .env ファイルで API_PORT=8001 に変更

# 解決方法2: ポートを使用しているプロセスを停止
lsof -i :8000
kill -9 <PID>
```

### データベース接続エラー

```bash
# PostgreSQLコンテナが起動しているか確認
docker-compose ps postgres

# PostgreSQLのログを確認
docker-compose logs postgres

# PostgreSQLの再起動
docker-compose restart postgres

# ヘルスチェックの状態確認
docker-compose ps
```

### マイグレーションエラー

```bash
# マイグレーション状態の確認
docker-compose exec api alembic current

# マイグレーションを最初から適用し直す
docker-compose exec api alembic downgrade base
docker-compose exec api alembic upgrade head
```

### コンテナが起動しない

```bash
# 詳細なログを確認
docker-compose logs

# コンテナを削除して再作成
docker-compose down
docker-compose up -d

# イメージを再ビルド
docker-compose up -d --build
```

### ディスク容量不足

```bash
# 未使用のコンテナ、イメージ、ボリュームを削除
docker system prune -a --volumes

# 確認してから実行
docker system df
```

### パーミッションエラー

```bash
# Linuxでボリュームマウント時にパーミッションエラーが出る場合

# 解決方法: docker-compose.yml に user を追加
# services:
#   api:
#     user: "${UID}:${GID}"

# または、コンテナ内でファイルの所有者を変更
docker-compose exec api chown -R 1000:1000 /app
```

## 本番環境での使用

本番環境では以下の変更を推奨します：

1. **ボリュームマウントの削除**
   ```yaml
   # docker-compose.yml から以下を削除
   # volumes:
   #   - ./app:/app/app
   #   - ./alembic:/app/alembic
   ```

2. **デバッグモードの無効化**
   ```env
   DEBUG=False
   ```

3. **リロードの無効化**
   ```yaml
   # docker-compose.yml のコマンドを変更
   command: uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. **環境変数の適切な管理**
   - `.env` ファイルをGitにコミットしない
   - 本番環境の認証情報を使用

5. **セキュリティ設定の強化**
   - CORS設定を本番環境のURLに限定
   - PostgreSQLのポートを外部に公開しない（`ports` セクションを削除）

## 参考リンク

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)

---

**作成日**: 2026-01-27  
**バージョン**: 1.0.0
