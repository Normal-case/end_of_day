from django.forms import ModelForm
from django.forms.widgets import MediaOrderConflictWarning
from diaryapp.models import Diary
from django import forms
from django_summernote.widgets import SummernoteWidget

class DiaryCreationForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'feeling','content']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'content': SummernoteWidget()
        }

class DiaryUpdateForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'feeling', 'date', 'content']
        widgets = {
            'content': SummernoteWidget()
        }
    date = forms.CharField(disabled=True)