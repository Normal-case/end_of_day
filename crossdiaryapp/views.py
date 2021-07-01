from django.shortcuts import render
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import CrossDiary, CrossDiaryContent
from .forms import DiarySearch, CrossDiaryCreationForm, CrossDiaryUpdateForm
from .calendar import Calendar
from .decorator import account_ownership_nickname, account_ownership_crossdiarykey
from django.db.models import Q

import calendar
from datetime import datetime, timedelta

@method_decorator(login_required, 'get')
class CrossDiaryList(View):
    def get(self, *args, **kwargs):
        nickname=self.request.user.profile.nickname
        cross = CrossDiary.objects.filter(Q(user_a=nickname) | Q(user_b=nickname))
        print(cross)
        return render(self.request, 'crossdiaryapp/list.html', {'cross':cross})

@method_decorator([login_required] + [account_ownership_nickname], 'get')
class HomeView(View):
    def get(self, *args, **kwargs):
        now = datetime.now()
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        cal = Calendar(now.year, now.month, user_a, user_b)
        html_cal = cal.formatmonth(withyear=True)
        current = f'{now.year}-{now.month}-{now.day}'
        form = DiarySearch()
        return render(self.request, 'crossdiaryapp/home.html', {'calendar':html_cal, 'now':current, 'form':form, 'user_a':user_a, 'user_b':user_b})

    def post(self, *args, **kwargs):
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        if 'prev_month' in self.request.POST:
            str_today = self.request.POST['current'].split('-')
            today = datetime.strptime(f'{str_today[0]}-{str_today[1]}-{str_today[2]}', '%Y-%m-%d')
            first = today.replace(day=1)
            prev_month = first - timedelta(days=1)
            cal = Calendar(prev_month.year, prev_month.month, user_a, user_b)
            html_cal = cal.formatmonth(withyear=True)
            current = f'{prev_month.year}-{prev_month.month}-{prev_month.day}'
            form = DiarySearch()
        elif 'next_month' in self.request.POST:
            str_today = self.request.POST['current'].split('-')
            today = datetime.strptime(f'{str_today[0]}-{str_today[1]}-{str_today[2]}', '%Y-%m-%d')
            day_in_month = calendar.monthrange(today.year, today.month)[1]
            first = today.replace(day=day_in_month)
            next_month = first + timedelta(days=1)
            cal = Calendar(next_month.year, next_month.month, user_a, user_b)
            html_cal = cal.formatmonth(withyear=True)
            current = f'{next_month.year}-{next_month.month}-{next_month.day}'
            form = DiarySearch()
        elif 'search' in self.request.POST:
            str_today = self.request.POST['date'].split('-')
            today = datetime.strptime(f'{str_today[0]}-{str_today[1]}-{str_today[2]}', '%Y-%m-%d')
            cal = Calendar(today.year, today.month, user_a, user_b)
            html_cal = cal.formatmonth(withyear=True)
            current = f'{today.year}-{today.month}-{today.day}'
            form = DiarySearch()
        return render(self.request, 'crossdiaryapp/home.html', {'calendar':html_cal,'now':current, 'form':form, 'user_a':user_a, 'user_b':user_b})

@method_decorator([login_required] + [account_ownership_nickname], 'get')
class CrossDiaryCreate(View):
    def get(self, *args, **kwargs):
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        c_year, c_month, c_day = self.kwargs['year'], self.kwargs['month'], self.kwargs['day']
        return render(self.request, 'crossdiaryapp/create.html', {'year':c_year, 'month':c_month, 'day':c_day, 'user_a':user_a, 'user_b':user_b})


@method_decorator([login_required] + [account_ownership_nickname], 'get')
@method_decorator([login_required] + [account_ownership_nickname], 'post')
class CrossDiaryCreateCommon(View):
    template_name = 'crossdiaryapp/create_common.html'
    form_class = CrossDiaryCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        return render(request, self.template_name, {'form': form, 'year':self.kwargs['year'], 'month': self.kwargs['month'], 'day':self.kwargs['day'], 'user_a':user_a, 'user_b':user_b})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        cross = CrossDiary.objects.get(user_a=user_a, user_b=user_b)
        if form.is_valid():
            temp_diary = form.save(commit=False)
            temp_diary.cross = cross
            temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
            temp_diary.save()
            return HttpResponseRedirect(reverse('crossdiaryapp:read', kwargs={'pk':temp_diary.pk}))
        return render(request, self.template_name, {'form':form})

@method_decorator([login_required] + [account_ownership_nickname], 'get')
@method_decorator([login_required] + [account_ownership_nickname], 'post')
class CrossDiarySelectFeeling(View):
    def get(self, request, *args, **kwargs):
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        c_year, c_month, c_day = self.kwargs["year"], self.kwargs["month"], self.kwargs["day"]
        return render(request, 'crossdiaryapp/select_feeling.html', {'year':c_year, 'month': c_month, 'day':c_day, 'user_a':user_a, 'user_b':user_b})

    def post(self, *args, **kwargs):
        user_a, user_b = self.kwargs['user_a'], self.kwargs['user_b']
        cross = CrossDiary.objects.get(user_a=user_a, user_b=user_b)
        if 'joy' in self.request.POST:
            temp_diary = CrossDiaryContent(cross=cross)
            temp_diary.title = f'{self.kwargs["month"]}월 {self.kwargs["day"]}일 일기'
            temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
            temp_diary.feeling = 'joy'
            temp_diary.save()
        elif 'sad' in self.request.POST:
            temp_diary = CrossDiaryContent(cross=cross)
            temp_diary.title = f'{self.kwargs["month"]}월 {self.kwargs["day"]}일 일기'
            temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
            temp_diary.feeling = 'sad'
            temp_diary.save()
        elif 'angry' in self.request.POST:
            temp_diary = CrossDiaryContent(cross=cross)
            temp_diary.title = f'{self.kwargs["month"]}월 {self.kwargs["day"]}일 일기'
            temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
            temp_diary.feeling = 'angry'
            temp_diary.save()
        else:
            temp_diary = CrossDiaryContent(cross=cross)
            temp_diary.title = f'{self.kwargs["month"]}월 {self.kwargs["day"]}일 일기'
            temp_diary.date = datetime.strptime(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}", "%Y-%m-%d")
            temp_diary.feeling = 'fear'
            temp_diary.save()
        return HttpResponseRedirect(reverse('crossdiaryapp:select_who', kwargs={'pk':temp_diary.pk}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectWho(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'crossdiaryapp/select_who.html', {'pk':self.kwargs['pk']})
    
    def post(self, *args ,**kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
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
        return HttpResponseRedirect(reverse('crossdiaryapp:select_when', kwargs={'pk':self.kwargs['pk']}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectWhen(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_when.html', {'pk':pk})
    
    def post(self, *args, **kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
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
        return HttpResponseRedirect(reverse('crossdiaryapp:select_where', kwargs={'pk':self.kwargs['pk']}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectWhere(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_where.html', {'pk':pk})
    
    def post(self, *args, **kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
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
        return HttpResponseRedirect(reverse('crossdiaryapp:select_what', kwargs={'pk':self.kwargs['pk']}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectWhat(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_what.html', {'pk':pk})
    
    def post(self, *args, **kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('crossdiaryapp:select_how', kwargs={'pk':self.kwargs['pk']}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectHow(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_how.html', {'pk':pk})
    
    def post(self, *args, **kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('crossdiaryapp:select_why', kwargs={'pk':self.kwargs['pk']}))


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiarySelectWhy(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_why.html', {'pk':pk})
    
    def post(self, *args, **kwargs):
        target_diary = CrossDiaryContent.objects.get(pk=self.kwargs['pk'])
        target_diary.content += ' ' + self.request.POST['self_input']
        target_diary.save()
        return HttpResponseRedirect(reverse('crossdiaryapp:select_continue', kwargs={'pk':self.kwargs['pk']}))

@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
class CrossDiarySelectContinue(View):
    def get(self, request, pk):
        return render(request, 'crossdiaryapp/select_continue.html', {'pk':pk})

@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
class CrossDiaryRead(DetailView):
    model = CrossDiaryContent
    context_object_name = 'target_diary'
    template_name = 'crossdiaryapp/detail.html'

@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiaryUpdateView(UpdateView):
    model = CrossDiaryContent
    context_object_name = 'target_diary'
    form_class = CrossDiaryUpdateForm
    template_name = 'crossdiaryapp/update.html'

    def get_success_url(self):
        return reverse('crossdiaryapp:read', kwargs={'pk': self.object.pk})


@method_decorator([login_required] + [account_ownership_crossdiarykey], 'get')
@method_decorator([login_required] + [account_ownership_crossdiarykey], 'post')
class CrossDiaryDeleteView(DeleteView):
    model = CrossDiaryContent
    template_name = 'crossdiaryapp/delete.html'
    context_object_name = 'target_diary'

    def get_success_url(self, *args, **kwargs):
        return reverse('crossdiaryapp:home', kwargs={'user_a':self.object.cross.user_a, 'user_b':self.object.cross.user_b})