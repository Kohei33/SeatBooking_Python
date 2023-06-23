import datetime
import re
from django.http import HttpResponseRedirect
from django.views import generic
from reserve.models import Schedule, Memo
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .modules.module import ForDelete
from reserve.consts import *

class MyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reserve/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule_list = []
        memo_list = []
        today = datetime.date.today()
        mymessages = []
        mymessages.append(MYPAGE_MESSAGE_1)
        mymessages.append(MYPAGE_MESSAGE_1)
        btnlabel_del = MYPAGE_LABEL_DEL
        mypage_title_1 = MYPAGE_TITLE_1
        mypage_title_2 = MYPAGE_TITLE_2
        mypage_title_3 = MYPAGE_TITLE_3

        # 予約一覧の
        # 過去のデータを表示する/表示しないボタン押下時
        if self.kwargs.get('seat_or_memo') == "seat":
            # 予約一覧
            # ボタン表示に従って結果を表示する
            # 過去のデータを表示するボタン押下時
            if self.kwargs['seat_past'] == 'seat_past_true':
                schedules = Schedule.objects.filter(user=self.request.user).order_by('date')
                seat_past = "seat_past_false"
                btnlabel_seat = MYPAGE_LABEL_2
            # 過去のデータを表示しないボタン押下時
            else:
                schedules = Schedule.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                seat_past = "seat_past_true"
                btnlabel_seat = MYPAGE_LABEL_1
            # メモ一覧
            # ボタン押下されていないので、変化なし
            if self.kwargs['memo_past'] == 'memo_past_true':
                memos = Memo.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                memo_past = "memo_past_true"
                btnlabel_memo = MYPAGE_LABEL_1
            else:
                memos = Memo.objects.filter(user=self.request.user).order_by('date')
                memo_past = "memo_past_false"
                btnlabel_memo = MYPAGE_LABEL_2
        # メモ一覧の
        # 過去のデータを表示する/表示しないボタン押下時
        elif self.kwargs.get('seat_or_memo') == "memo":
            # 予約一覧
            # ボタン押下されていないので、変化なし
            if self.kwargs['seat_past'] == 'seat_past_true':
                schedules = Schedule.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                seat_past = "seat_past_true"
                btnlabel_seat = MYPAGE_LABEL_1
            else:
                schedules = Schedule.objects.filter(user=self.request.user).order_by('date')
                seat_past = "seat_past_false"
                btnlabel_seat = MYPAGE_LABEL_2
            # メモ一覧
            # ボタン表示に従って結果を表示する
            # 過去のデータを表示するボタン押下時
            if self.kwargs['memo_past'] == 'memo_past_true':
                memos = Memo.objects.filter(user=self.request.user).order_by('date')
                memo_past = "memo_past_false"
                btnlabel_memo = MYPAGE_LABEL_2
            #過去のデータを表示しないボタン押下時
            else:
                memos = Memo.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                memo_past = "memo_past_true"
                btnlabel_memo = MYPAGE_LABEL_1
        # 過去のデータを表示する/しないボタン押下以外の時
        # ボタン押下されていないので、変化なし
        else:
            # 予約一覧
            if self.kwargs['seat_past'] == 'seat_past_true':
                schedules = Schedule.objects.filter(user=self.request.user).order_by('date')
                seat_past = "seat_past_false"
                btnlabel_seat = MYPAGE_LABEL_2
            else:
                schedules = Schedule.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                seat_past = "seat_past_true"
                btnlabel_seat = MYPAGE_LABEL_1
            # メモ一覧
            if self.kwargs['memo_past'] == 'memo_past_true':
                memos = Memo.objects.filter(user=self.request.user).order_by('date')
                memo_past = "memo_past_false"
                btnlabel_memo = MYPAGE_LABEL_2
            else:
                memos = Memo.objects.filter(user=self.request.user, date__gte=today).order_by('date')
                memo_past = "memo_past_true"
                btnlabel_memo = MYPAGE_LABEL_1

        for schedule in schedules:
            if_schedule_future = True
            if schedule.date < datetime.date.today():
                if_schedule_future = False
            schedule_list.append((schedule, if_schedule_future))
        
        for memo in memos:
            if_memo_future = True
            if memo.date < datetime.date.today():
                if_memo_future = False
            memo_list.append((memo, if_memo_future))
        
        context['mypage_title_1'] = mypage_title_1
        context['mypage_title_2'] = mypage_title_2
        context['mypage_title_3'] = mypage_title_3
        context['schedule_list'] = schedule_list
        context['memo_list'] = memo_list
        context['seat_past'] = seat_past
        context['memo_past'] = memo_past
        context['btnlabel_seat'] = btnlabel_seat
        context['btnlabel_memo'] = btnlabel_memo
        context['btnlabel_del'] = btnlabel_del
        context['mymessages'] = mymessages
        return context

    def post(self, request, **kwargs):
        # 予約の削除
        if request.POST.get('seat_or_memo') == "seat":
            # 削除対象のオブジェクトを連結文字列のリストとして受け取る
            schedules_to_del = request.POST.getlist('checks_del')
            for schedule_to_del in schedules_to_del:
                # 連結文字列を分割する
                id = ForDelete.string_spliter_for_del(schedule_to_del)
                if not Schedule.objects.filter(id=id).exists():
                    messages.error(request, ERROR_2)
                else:
                    Schedule.objects.filter(id=id).delete()
            # True/Falseの状態を逆にしてから同じページにgetアクセスする
            if "seat_past_true" in request.path_info:
                path = re.sub(r"seat_past_true", "seat_past_false", request.path_info)
            elif "seat_past_false" in request.path_info:
                path = re.sub(r"seat_past_false", "seat_past_true", request.path_info)

        # メモの削除
        elif request.POST.get('seat_or_memo') == "memo":
            # 削除対象のオブジェクトを連結文字列のリストとして受け取る
            memos_to_del = request.POST.getlist('checks_del')
            for memo_to_del in memos_to_del:
                # 連結文字列を分割する
                id = ForDelete.string_spliter_for_del(memo_to_del)
                if not Memo.objects.filter(id=id).exists():
                    messages.error(request, ERROR_2)
                else:
                    Memo.objects.filter(id=id).delete()
            # True/Falseの状態を逆にしてから同じページにgetアクセスする
            if "memo_past_true" in request.path_info:
                path = re.sub(r"memo_past_true", "memo_past_false", request.path_info)
            elif "memo_past_false" in request.path_info:
                path = re.sub(r"memo_past_false", "memo_past_true", request.path_info)

        return HttpResponseRedirect(path)