from django.forms import ModelForm
from django import forms
from profileapp.models import Profile

class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'phone_number', 'birth', 'profile_image']
        widgets = {
            'birth': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ex)"-" 빼고 작성해주세요'})
        self.fields['nickname'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':' '})