# fightmatch

fightmatch は、武道・格闘技の練習者が「なぜ始めたか」「なぜ続けているか」「試合に出たいか」を回答し、目的に応じたマッチングや提案につなげるための診断アプリです。

現在は開発途中の MVP です。基本質問の表示、回答送信、回答保存を中心に実装しています。

## 現在実装されている機能

- 基本質問の取得 API
  - `GET /api/purpose/questions/basic`
  - PostgreSQL / SQLite 上の質問データを返却
- 選択質問の取得 API
  - `GET /api/purpose/questions/choice`
  - 「試合に出てみたいか」などの質問データを返却
- 回答保存 API
  - `POST /api/purpose/answers`
  - 選択式の複数回答と自由記述を保存
  - 存在しない質問 ID は `404` で拒否
- Vue フロントエンド
  - `/question` で基本質問を表示
  - 「その他」を選んだ場合のみ自由記述欄を表示
  - 必須の選択式質問に回答するまで次へ進めない制御
  - 基本質問の回答を API に送信
  - 固定データによる「試合に出てみたいか」の選択画面
  - `/result` で回答完了画面を表示
- 開発用データ投入
  - `python -m purpose.seed` で質問と開発用ユーザーを登録
- テスト
  - FastAPI の質問取得・回答保存テスト
  - PostgreSQL JSONB 保存の任意実行テスト
  - Vue コンポーネントと回答状態管理のテスト

## 未実装・開発途中の点

- 回答結果をもとにしたマッチングや推薦ロジックは未実装です。
- Vue の選択質問画面は、現時点では API 取得ではなくコンポーネント内の固定データを使っています。
- Flutter アプリは初期構成に近く、FastAPI への疎通確認用画面のみです。
- 認証や本番向けのユーザー管理は未実装です。回答保存では開発用ユーザー ID を使用しています。

## 使用技術

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL / SQLite
- psycopg2
- pytest
- Uvicorn

### Web Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Vitest
- Vue Test Utils
- ESLint / Prettier

### Mobile App

- Flutter
- Dart
- http package

### Infrastructure / Development

- Docker
- Docker Compose
- PostgreSQL 16 Alpine

## ディレクトリ構成

```text
backend/   FastAPI API、DB モデル、シード、テスト
web/       Vue 3 + Vite の Web フロントエンド
app/       Flutter アプリ
```

## ローカル開発

### PostgreSQL を起動

```bash
docker compose up -d postgres
```

### バックエンドの開発データを投入

```bash
cd backend
DATABASE_URL=postgresql+psycopg2://fightmatch:fightmatch@localhost:5432/fightmatch \
  python -m purpose.seed
```

### FastAPI を起動

```bash
cd backend
DATABASE_URL=postgresql+psycopg2://fightmatch:fightmatch@localhost:5432/fightmatch \
  uvicorn main:app --reload
```

### Web フロントエンドを起動

```bash
cd web
npm install
npm run dev
```

Web フロントエンドは `http://127.0.0.1:8000` の API にリクエストします。

## テスト

### Backend

```bash
cd backend
python -m pytest
```

PostgreSQL 連携テストは、環境変数を指定した場合のみ実行されます。

```bash
cd backend
RUN_POSTGRES_TESTS=1 \
TEST_DATABASE_URL=postgresql+psycopg2://fightmatch:fightmatch@localhost:5432/fightmatch_test \
  python -m pytest test_purpose_postgres_integration.py
```

### Web Frontend

```bash
cd web
npm run test
```
