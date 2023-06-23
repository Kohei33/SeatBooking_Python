import datetime
import re
from django.shortcuts import get_object_or_404
from django.views import generic
from reserve.models import Seat, Schedule, Memo
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .modules.module import CreateCalendar, ForMultiChoice, ShowMemoInCalendar
from reserve.consts import *

class MultiChoice(LoginRequiredMixin, generic.ListView):
    template_name = 'reserve/multi_choice.html'
    model = Seat
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seats = Seat.objects.all()
        messages = []
        today = datetime.date.today()

        if self.kwargs.get('dir'):
            dir = self.kwargs.get('dir')
        else:
            dir = ""
        
        if self.kwargs.get('date'):
            date = self.kwargs['date']
        else:
            date = ""

        #画面表示する最初と最後の日を取得する
        start_date, end_date, days, days_isHoliday, msg = CreateCalendar.get_start_and_end_date(dir, date)
        messages.append(msg)

        #各席の予約状況を取得する
        seat, seats_days = CreateCalendar.get_seat_available_or_not(seats, days)

        #画面表示するメモを取得する
        users_days_memos = ShowMemoInCalendar.get_filtered_memos(start_date, end_date, days)

        context["seats"] = seats
        context["seat"] = seat
        context["days_isHoliday"] = days_isHoliday
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["dir1"] = DIR_1
        context["dir2"] = DIR_2
        context["messages"] = messages
        context["today"] = today
        context["seats_days"] = seats_days
        context["days"] = days
        context["users_days_memos"] = users_days_memos

        return context
    
    #複数予約処理
    def post(self, request, **kwargs):
        # 予約情報を連結文字列のリストとして受け取る
        checks_value = request.POST.getlist('checks')
        for value in checks_value:
            #渡された連結文字列を分割する
            seat_pk, year, month, day, if_enable, reserve_user = ForMultiChoice.string_spliter(value)
            #型を文字列から数値に変換する
            year = int(year);month = int(month);day = int(day)
            
            seat = get_object_or_404(Seat, pk=seat_pk)
            date = datetime.date(year=year, month=month, day=day)
            if Schedule.objects.filter(seat=seat, date=date).exists():
                messages.error(request, ERROR_1)
            else:
                Schedule.objects.create(seat=seat, date=date, user=request.user)
        #予約実行したページを再表示
        # return HttpResponseRedirect(request.path_info)
        return self.get(request)