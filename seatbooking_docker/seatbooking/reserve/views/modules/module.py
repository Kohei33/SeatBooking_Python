import datetime
import unicodedata
import jpholiday
import re
from reserve.models import Schedule, Memo
from django.contrib.auth.models import User

#カレンダー表示
class CreateCalendar():
    #画面表示する最初と最後の日を取得する
    def get_start_and_end_date (dir, date):
        msg = ""
        today = datetime.date.today()
        days_isHoliday = []
        if dir == "before": #前の日付に移動したとき
            if date <= datetime.date(year=1, month=1, day=8): # 境界値
                start_date = today - datetime.timedelta(days=60)
                msg = "確認できるのは60日前までです。"
            else:
                start_date = date - datetime.timedelta(days=7)
                if start_date >= today + datetime.timedelta(days=24):
                        start_date = today + datetime.timedelta(days=24)
                        msg = "確認できるのは30日後までです。"
                elif start_date <= today - datetime.timedelta(days=60):
                    start_date = today - datetime.timedelta(days=60)
                    msg = "確認できるのは60日前までです。"
        elif dir == "future": #後の日付に移動したとき
            if date >= datetime.date(year=9999, month=12, day=24): # 境界値
                start_date = today + datetime.timedelta(days=24)
                msg = "確認できるのは30日後までです。"
            else:
                start_date = date + datetime.timedelta(days=7)
                if start_date >= today + datetime.timedelta(days=24):
                    start_date = today + datetime.timedelta(days=24)
                    msg = "確認できるのは30日後までです。"
                elif start_date <= today - datetime.timedelta(days=60):
                    start_date = today - datetime.timedelta(days=60)
                    msg = "確認できるのは60日前までです。"
        else: #初期表示のとき
            start_date = today
        days = [start_date + datetime.timedelta(days=day) for day in range(7)]
        #休日判定
        for day in days:
            isHoliday = jpholiday.is_holiday(day) or day.weekday() >= 5
            days_isHoliday.append((day, isHoliday))
        end_date = days[-1]
        return start_date, end_date, days, days_isHoliday, msg
    
    #各席の予約状況を取得する
    def get_seat_available_or_not (seats, days):
        seats_days = [] #席ごとのリスト・1次元目
        today = datetime.date.today()
        for seat in seats:
            days_if_enable = [] #日付ごとのリスト・2次元目
            for day in days:
                #各席・各日の予約可否を取得する
                #予約が埋まっていない、かつ現在日以降の場合、予約可
                if not Schedule.objects.filter(seat=seat, date=day).exists() and day >= today:
                    if_enable = True
                    reserve_user = ""
                else: #上記の場合以外は予約不可
                    if_enable = False
                    if Schedule.objects.filter(seat=seat, date=day).exists(): #予約者がいる場合
                        reserve_user = Schedule.objects.get(seat=seat, date=day).user #予約者を取得
                    else:
                        reserve_user = "×" #予約者がいない場合、×を格納する
                days_if_enable.append((day, if_enable, reserve_user)) #日付ごとのリスト(2次元目)に値をセット
            seats_days.append((seat, days_if_enable)) #席ごとのリスト(1次元目)に値をセット
        return seat, seats_days

#複数日の予約
class ForMultiChoice():
    #予約のための連結文字列を分割する関数
    # 引数の例
    # 1&(datetime.date(2023, 6, 5), True, '')
    def string_spliter (value):
        #席とそれに紐づく情報を分割
        s_value = value.split('&')
        #席を戻り値にセット
        seat_pk = s_value[0]
        #席に紐づく情報を分割
        s_s_value = s_value[1].split(',')
        #戻り値セット
        year = re.sub(r"\D", "", s_s_value[0]) #年
        month = re.sub(r"\D", "", s_s_value[1]) #月
        day = re.sub(r"\D", "", s_s_value[2]) #日
        if_enable = s_s_value[3] #予約可否
        reserve_user = s_s_value[4] #予約者
        return seat_pk, year, month, day, if_enable, reserve_user

#予約取消
class ForDelete():
    #取消のための連結文字列を分割する関数
    def string_spliter_for_del (value):
        #スペースと>で分割
        s_value = value.split(' ')
        ss_value = s_value[1].split('>')
        id = ss_value[0] #ID
        return id

#カレンダー形式でメモ表示
class ShowMemoInCalendar():
    def get_filtered_memos (start_date, end_date, days):
        users = User.objects.all()
        users_if_memos = []
        for user in users:
            if Memo.objects.filter(user=user, date__range=[start_date, end_date]):
                users_if_memos.append(user)

        # 配列１を作成
        # 前の処理で抽出したユーザのみを対象とする
        users_days_memos = []
        for user in users_if_memos:
            #画面表示する日付ごとの配列２を作成
            user_days_memos = []
            for day in days:
                # 指定したユーザと日付でメモが存在するか判定
                if Memo.objects.filter(user=user, date=day).exists:
                    # メモを格納した配列３を作成
                    user_day_memos = []
                    memos = Memo.objects.filter(user=user, date=day)
                    for memo in memos:
                        # タイトルの12バイト目以降は省略する
                        memo_title = memo.title
                        memo_len, if_multibyte = ShowMemoInCalendar.len_count(memo_title)
                        if memo_len > 12:
                            if if_multibyte:
                                memo_title = memo_title[0:6] + "…"
                            else:
                                memo_title = memo_title[0:11] + "…"
                        # 配列３に格納
                        user_day_memos.append((memo.id, memo_title))
                
                # 日付と配列３のタプルを配列２に格納
                user_days_memos.append((day, user_day_memos))
            
            # ユーザと配列２のタプルを配列１に格納
            users_days_memos.append((user, user_days_memos))
        return users_days_memos
    
    # 文字数カウント
    # 1バイトにつき1文字とカウントする
    def len_count(text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 2
                if_multibyte = True
            else:
                count += 1
                if_multibyte = False
        return count, if_multibyte