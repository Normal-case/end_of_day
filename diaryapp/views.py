from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView, DetailView
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.edit import UpdateView, DeleteView
from .calendar import Calendar
from .models import Diary
from .forms import DiaryCreationForm, DiaryUpdateForm

# Create your views here.
@method_decorator(login_required, 'get')
class HomeView(View):
    def get(self, request):
        now = datetime.now()
        cal = Calendar(now.year, now.month, request.user)
        html_cal = cal.formatmonth(withyear=True)
        return render(request, 'diaryapp/home.html', {'calendar':html_cal})

class DiaryCreate(View):
    def get(self, request, year, month, day):
        c_year, c_month, c_day = year, month, day
        return render(request, 'diaryapp/create.html', {'year':c_year, 'month':c_month, 'day':c_day})

class DiaryCreateCommon(CreateView):
    model = Diary
    context_object_name = 'target_diary'
    template_name = 'diaryapp/create_common.html'
    form_class = DiaryCreationForm

    def form_valid(self, form):
        temp_diary = form.save(commit=False)
        temp_diary.user = self.request.user
        temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
        temp_diary.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        value = super(DiaryCreateCommon, self).get_context_data(**kwargs)
        value['year'] = self.kwargs['year']
        value['month'] = self.kwargs['month']
        value['day'] = self.kwargs['day']
        return value

    def get_success_url(self):
        return reverse('diaryapp:read', kwargs={'pk':self.object.pk})

class DiarySelectFeeling(View):
    def get(self, request, year, month, day):
        c_year, c_month, c_day = year, month, day
        return render(request, 'diaryapp/select_feeling.html', {'year':c_year, 'month': c_month, 'day':c_day})

    def post(self, request, year, month, day):
        print('post까지 들어옴')
        if 'joy' in self.request.POST:
            print('joy')
            temp_diary = Diary(user=self.request.user)
            temp_diary.title = f'{month}월 {day}일 일기'
            temp_diary.date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            temp_diary.feeling = 'joy'
            temp_diary.save()
        elif 'sad' in self.request.POST:
            print('sad')
            temp_diary = Diary(user=self.request.user)
            temp_diary.title = f'{month}월 {day}일 일기'
            temp_diary.date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            temp_diary.feeling = 'sad'
            temp_diary.save()
        elif 'angry' in self.request.POST:
            print('angry')
            temp_diary = Diary(user=self.request.user)
            temp_diary.title = f'{month}월 {day}일 일기'
            temp_diary.date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            temp_diary.feeling = 'angry'
            temp_diary.save()
        else:
            print('fear')
            temp_diary = Diary(user=self.request.user)
            temp_diary.title = f'{month}월 {day}일 일기'
            temp_diary.date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            temp_diary.feeling = 'fear'
            temp_diary.save()
        print('리턴 바로앞!')
        return HttpResponseRedirect(reverse('diaryapp:select_who', kwargs={'pk':temp_diary.pk}))

class DiarySelectWho(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_who.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        if target_diary.content:
            if 'me' in self.request.POST:
                target_diary.content += '<br>내가'
                target_diary.save()
            elif 'friend' in self.request.POST:
                target_diary.content += '<br>친구가'
                target_diary.save()
            elif 'father' in self.request.POST:
                target_diary.content += '<br>아빠가'
                target_diary.save()
            elif 'mother' in self.request.POST:
                target_diary.content += '<br>엄마가'
                target_diary.save()
            elif 'girlfriend' in self.request.POST:
                target_diary.content += '<br>여친이'
                target_diary.save()
            elif 'boyfriend' in self.request.POST:
                target_diary.content += '<br>남친이'
                target_diary.save()
            elif 'etc' in self.request.POST:
                target_diary.content += '<br>' + self.request.POST['self_input']
                target_diary.save()
        else:
            if 'me' in self.request.POST:
                target_diary.content = '내가'
                target_diary.save()
            elif 'friend' in self.request.POST:
                target_diary.content = '친구가'
                target_diary.save()
            elif 'father' in self.request.POST:
                target_diary.content = '아빠가'
                target_diary.save()
            elif 'mother' in self.request.POST:
                target_diary.content = '엄마가'
                target_diary.save()
            elif 'girlfriend' in self.request.POST:
                target_diary.content = '여친이'
                target_diary.save()
            elif 'boyfriend' in self.request.POST:
                target_diary.content = '남친이'
                target_diary.save()
            elif 'etc' in self.request.POST:
                target_diary.content = self.request.POST['self_input']
                target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_when', kwargs={'pk':pk}))

class DiarySelectWhen(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_when.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        if 'before_noon' in self.request.POST:
            target_diary.content += ' 오전에'
            target_diary.save()
        elif 'after_noon' in self.request.POST:
            target_diary.content += ' 오후에'
            target_diary.save()
        elif 'morning' in self.request.POST:
            target_diary.content += ' 아침에'
            target_diary.save()
        elif 'noon' in self.request.POST:
            target_diary.content += ' 점심에'
            target_diary.save()
        elif 'evening' in self.request.POST:
            target_diary.content += ' 저녁에'
            target_diary.save()
        elif 'night' in self.request.POST:
            target_diary.content += ' 밤에'
            target_diary.save()
        elif 'etc' in self.request.POST:
            target_diary.content += ' ' + self.request.POST['self_input']
            target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_where', kwargs={'pk':pk}))

class DiarySelectWhere(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_where.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        if 'home' in self.request.POST:
            target_diary.content += ' 집에서'
            target_diary.save()
        elif 'school' in self.request.POST:
            target_diary.content += ' 학교에서'
            target_diary.save()
        elif 'company' in self.request.POST:
            target_diary.content += ' 직장에서'
            target_diary.save()
        elif 'park' in self.request.POST:
            target_diary.content += ' 공원에서'
            target_diary.save()
        elif 'restaurant' in self.request.POST:
            target_diary.content += ' 식당에서'
            target_diary.save()
        elif 'cafe' in self.request.POST:
            target_diary.content += ' 카페에서'
            target_diary.save()
        elif 'etc' in self.request.POST:
            target_diary.content += ' ' + self.request.POST['self_input']
            target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_what', kwargs={'pk':pk}))

class DiarySelectWhat(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_what.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_how', kwargs={'pk':pk}))

class DiarySelectHow(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_how.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_why', kwargs={'pk':pk}))

class DiarySelectWhy(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_why.html', {'pk':pk})
    
    def post(self, request, pk):
        target_diary = Diary.objects.get(pk=pk)
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('diaryapp:select_continue', kwargs={'pk':pk}))

class DiarySelectContinue(View):
    def get(self, request, pk):
        return render(request, 'diaryapp/select_continue.html', {'pk':pk})

class DiaryRead(DetailView):
    model = Diary
    context_object_name = 'target_diary'
    template_name = 'diaryapp/detail.html'


class DiaryUpdateView(UpdateView):
    model = Diary
    context_object_name = 'target_diary'
    form_class = DiaryUpdateForm
    template_name = 'diaryapp/update.html'

    def get_success_url(self):
        return reverse('diaryapp:read', kwargs={'pk': self.object.pk})


class DiaryDeleteView(DeleteView):
    model = Diary
    success_url = reverse_lazy('diaryapp:home')
    template_name = 'diaryapp/delete.html'
    context_object_name = 'target_diary'
