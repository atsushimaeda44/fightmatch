# frontend/Dockerfile
FROM flutter/flutter:latest

# 作業ディレクトリの設定
WORKDIR /app

# Flutter のパッケージをインストール
COPY pubspec.yaml .
RUN flutter pub get

# アプリコードをコピー
COPY . .

# Flutter のビルド
RUN flutter build apk

# サーバーの起動
CMD ["flutter", "run"]
