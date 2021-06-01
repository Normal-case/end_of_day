from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from .forms import MyLoginForm

# Create your views here.
class AccountCreateView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/create.html'

class MyLoginView(LoginView):
    template_name = 'accountapp/login.html'
    authentication_form = MyLoginForm

    def get_success_url(self):
        return reverse('diaryapp:home')