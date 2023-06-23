from django.urls import path, register_converter
from .views import MyPageView, SeatLayoutView, MultiChoiceView, MemoDetailView, MemoCreateView, MemoUpdateView
from django.contrib.auth.views import LoginView, LogoutView
from datetime import date, datetime

app_name = 'reserve'

# GETパラメータでdate型を渡すためのconverter
class DateConverter:
  regex = r"\d{4}-\d{1,2}-\d{1,2}"
  format = "%Y-%m-%d"

  def to_python(self, value: str) -> date:
      return datetime.strptime(value, self.format).date()

  def to_url(self, value: date) -> str:
      return value.strftime(self.format)

register_converter(DateConverter, "date")

urlpatterns = [
    path('', MultiChoiceView.MultiChoice.as_view(), name='multi_choice'),
    path('<date:date>/<str:dir>', MultiChoiceView.MultiChoice.as_view(), name='multi_choice'),
    path('memodetail/<int:pk>', MemoDetailView.MemoDetail.as_view(), name='memo_detail'),
    path('memocreate/<date:date>', MemoCreateView.MemoCreate.as_view(), name='memo_form'),
    path('memoupdate/<int:pk>', MemoUpdateView.MemoUpdate.as_view(), name='memo_update'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/<str:seat_past>/<str:memo_past>/<str:seat_or_memo>', MyPageView.MyPage.as_view(), name='mypage'),
    path('seatlayout/', SeatLayoutView.SeatLayout.as_view(), name='seat_layout'),
]