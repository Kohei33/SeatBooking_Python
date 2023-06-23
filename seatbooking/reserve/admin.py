from django.contrib import admin
from .models import Seat, Schedule, Memo

admin.site.register(Seat)
admin.site.register(Schedule)
admin.site.register(Memo)