from django.urls import reverse_lazy
from django.views import generic
from reserve.forms import CreateMemo
from reserve.models import Memo

class MemoCreate(generic.CreateView):
    model = Memo
    template_name = 'reserve/memo_form.html'
    form_class = CreateMemo
    success_url = "/reserve"

    def get_form_kwargs(self):
        kwargs = super(MemoCreate, self).get_form_kwargs()
        kwargs['date'] = str(self.kwargs['date'])
        kwargs['seat'] = ""
        kwargs['user'] = self.request.user
        kwargs['title'] = ""
        kwargs['text'] = ""
        return kwargs
    
    # def post(self, form, **kwargs):
    #     self.request.POST.get
        
    #     checks_value = self.request.POST.getlist('checks')
    #     #チェック一件ごとに処理する
    #     for value in checks_value:
    #         #渡された連結文字列を分割する
    #         seat_pk, year, month, day, if_enable, reserve_user = ForMultiChoice.string_spliter(value)
    #         #型を文字列から数値に変換する
    #         year = int(year);month = int(month);day = int(day)
            
    #         seat = get_object_or_404(Seat, pk=seat_pk)
    #         date = datetime.date(year=year, month=month, day=day)
    #         if Schedule.objects.filter(seat=seat, date=date).exists():
    #             messages.error(self.request, ERROR_1)
    #         else:
    #             Schedule.objects.create(seat=seat, date=date, user=self.request.user)
    #     #予約実行したページを再表示
    #     return HttpResponseRedirect(self.request.path_info)
