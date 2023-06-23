#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# 環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
if [ $DEBUG = "True" ]
then
    python manage.py runserver 0.0.0.0:8000 --settings=seatbooking.settings_dev
else
    python manage.py collectstatic --noinput
    
    # 0.0.0.0を指定するとコンテナ上のすべてのネットワークインターフェースでlistenする
    # 127.0.0.1は自コンテナのlocalhostなので、ほかのコンテナから接続できない
    gunicorn seatbooking.wsgi:application --bind 0.0.0.0:8000
fi