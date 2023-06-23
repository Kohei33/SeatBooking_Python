from django.shortcuts import redirect
from django.views import generic
from reserve.models import Memo

class MemoDetail(generic.DetailView):
    model = Memo
    template_name = 'reserve/memo_detail.html'
    context_object_name = "memo_detail"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["login_user"] = self.request.user
        return context
    
    def post(self, request, **kwargs):
        Memo.objects.get(pk=kwargs['pk']).delete()
        return redirect('reserve:multi_choice')