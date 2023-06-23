# seatbooking_docker
## 座席予約ツール
- ログイン必須。

![ログイン](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/50a4fb80-e581-4ced-a931-6b79ae2aad4d)

- オフィス内の座席と日付を指定して利用予約する。

![予約](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/5ef2b6c4-473c-4f2e-b7e9-7bdb43b2c43d)

- 日付ごとにメモ登録可能。

![メモ登録](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/881febd7-78cc-495c-9d7e-763dcb368d89)

- マイページで自分の予約情報とメモを管理。

![マイページ](https://github.com/Kohei33/SeatBooking_Python/assets/63783758/7babdd14-a59e-406a-9def-88ae1f19d90a)

## 開発環境
- 開発環境はdocker-compose.dev.ymlを使ってビルドする
- `docker-compose -f docker-compose.dev.yml up -d --build`
- localhost:8000/reserveでトップページに接続できる
## 本番環境
- 本番環境はdocker-compose.prod.ymlを使ってビルドする
- `docker-compose -f docker-compose.prod.yml up -d --build`
- \[server]:50001/reserveでトップページに接続できる
