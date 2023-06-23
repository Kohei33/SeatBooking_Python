from django import forms
from .models import Memo

class CreateMemo(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ("date", "seat", "user", "title", "text")

    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop("date")
        self.seat = kwargs.pop("seat")
        self.user = kwargs.pop("user")
        self.title = kwargs.pop("title")
        self.text = kwargs.pop("text")
        super(CreateMemo, self).__init__(*args, **kwargs)
        self.fields['date'].initial = self.date
        self.fields['seat'].initial = self.seat
        self.fields['user'].initial = self.user
        self.fields['title'].initial = self.title
        self.fields['text'].initial = self.text