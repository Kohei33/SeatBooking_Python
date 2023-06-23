# seatbooking_docker
座席予約webサイト
### seatbookingフォルダは別途cloneが必要
## 開発環境
- 開発環境はdocker-compose.dev.ymlを使ってビルドする
- `docker-compose -f docker-compose.dev.yml up -d --build`
- localhost:8000/reserveでトップページに接続できる
- 変更作業は、ローカル環境にgit clone⇒env.devファイルを配置⇒コンテナを起動⇒VSCodeでAttach to running containerでコンテナに入って行う
- 変更はAuto reloadされるので即時確認できる。
## 本番環境
- 本番環境はdocker-compose.prod.ymlを使ってビルドする
- `docker-compose -f docker-compose.prod.yml up -d --build`
- \[server]:50001/reserveでトップページに接続できる
