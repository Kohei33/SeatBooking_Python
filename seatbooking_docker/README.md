# seatbooking_docker
## 座席予約ツール
- ログイン必須。

![ログイン](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/50a4fb80-e581-4ced-a931-6b79ae2aad4d)

- オフィス内の座席と日付を指定して利用予約する。

![予約](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/5ef2b6c4-473c-4f2e-b7e9-7bdb43b2c43d)

- 予約は30日後まで可能。過去60日までの予約状況を確認可能。
- 日付ごとにメモ登録可能。
- マイページで自分の予約情報とメモを管理。
## 開発環境
- 開発環境はdocker-compose.dev.ymlを使ってビルドする
- `docker-compose -f docker-compose.dev.yml up -d --build`
- localhost:8000/reserveでトップページに接続できる
## 本番環境
- 本番環境はdocker-compose.prod.ymlを使ってビルドする
- `docker-compose -f docker-compose.prod.yml up -d --build`
- \[server]:50001/reserveでトップページに接続できる
