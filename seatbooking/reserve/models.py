from django.db import models
from datetime import date
from django.utils import timezone
from django.conf import settings

class Seat(models.Model):
    name = models.CharField('席名', max_length=255)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    date = models.DateField('予約日')
    seat = models.ForeignKey('Seat', verbose_name='席', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='予約者', on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now)   # timezone is defined on setting.py

    def __str__(self):
        return f'{self.id}'

class Memo(models.Model):
    date = models.DateField('日付')
    seat = models.ForeignKey('Seat', verbose_name='席', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザ', on_delete=models.CASCADE, null=True)
    title = models.CharField('タイトル', max_length=255, null=True) 
    text = models.CharField('メモ', max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.id}'