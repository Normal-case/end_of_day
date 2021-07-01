from django.forms import ModelForm
from django.forms.widgets import MediaOrderConflictWarning
from .models import CrossDiaryContent
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.forms.widgets import NumberInput

class CrossDiaryCreationForm(ModelForm):
    class Meta:
        model = CrossDiaryContent
        fields = ['title', 'feeling','content']
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'content': SummernoteWidget()
        }

class CrossDiaryUpdateForm(ModelForm):
    class Meta:
        model = CrossDiaryContent
        fields = ['title', 'feeling', 'date', 'content']
        widgets = {
            'content': SummernoteWidget()
        }
    date = forms.CharField(disabled=True)

class DiarySearch(forms.Form):
    date = forms.DateField(widget=NumberInput(attrs={'type':'date'}), required=False)