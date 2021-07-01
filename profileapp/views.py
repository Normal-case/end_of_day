from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from profileapp.forms import ProfileCreationForm
from profileapp.models import Profile, Invite
from profileapp.decorator import account_ownership_username
from crossdiaryapp.models import CrossDiary
from diaryapp.models import Diary
from end_of_day import settings
from wordcloud import WordCloud
from collections import Counter
import re

@method_decorator([login_required] + [account_ownership_username], 'get')
@method_decorator([login_required] + [account_ownership_username], 'post')
class ProfileMain(View):
    def get(self, request, *args, **kwargs):
        target_user = self.request.user
        try:
            invite = Invite.objects.filter(profile=target_user.profile)
        except:
            invite = ""
        return render(request, 'profileapp/main.html', {'target_user':target_user, 'invite_message':invite})

    def post(self, *args, **kwargs):
        if 'search' in self.request.POST:
            target_user = self.request.user
            search = self.request.POST['search']
            user_list = ""
            if search:
                user_list = Profile.objects.filter(nickname__icontains=search)
        elif 'invite' in self.request.POST:
            target_user = self.request.user
            user_list = ""
            invite_user = self.request.POST['invite']
            target_profile = Profile.objects.get(nickname=invite_user)
            try:
                Invite.objects.get(profile=target_profile, sender=self.request.user.profile.nickname)
                messages.error(self.request, '이미 초대 메시지를 보냈습니다.')
            except:
                temp_invite = Invite()
                temp_invite.profile = target_profile
                temp_invite.sender = self.request.user.profile.nickname
                temp_invite.save()
                messages.success(self.request, '초대 메시지를 전송했습니다.')
        elif 'accept' in self.request.POST:
            invite = Invite.objects.get(profile=self.request.user.profile, sender=self.request.POST['sender'])
            cross = CrossDiary()
            cross.user_a = invite.sender
            cross.user_b = invite.profile.nickname
            cross.save()
            invite.delete()
            return HttpResponseRedirect(reverse('crossdiaryapp:list', kwargs={'id':self.request.user.username}))

        elif 'reject' in self.request.POST:
            user_list = ""
            invite = Invite.objects.get(profile=self.request.user.profile, sender=self.request.POST['sender'])
            invite.delete()
        return render(self.request, 'profileapp/main.html', {'target_user': target_user, 'search_user':user_list})

@method_decorator([login_required] + [account_ownership_username], 'get')
@method_decorator([login_required] + [account_ownership_username], 'post')
class ProfileCreate(CreateView):
    model = Profile
    context_object_name = 'target_profile'
    template_name = 'profileapp/create.html'
    form_class = ProfileCreationForm

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profileapp:main', kwargs={'id': self.object.user.username})

@method_decorator([login_required] + [account_ownership_username], 'get')
class Visualize(View):
    def get(self, *args, **kwargs):
        feeling_dict = {
            'joy':'기쁨',
            'angry':'화남',
            'sad':'슬픔',
            'fear':'두려움',
        }
        diary_list = Diary.objects.filter(user=self.request.user)

        if len(diary_list) == 0:
            html_path = ""
            data = ""

        else:
            raw = list()
            feel = list()
            for diary in diary_list:
                if diary.content:
                    raw.append(diary.content)
                feel.append(diary.feeling)
            counter = Counter(feel)
            data = list()
            for i in feeling_dict:
                data.append(counter[i])

            raw_html = ' '.join(raw)
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            clean_text = re.sub(cleanr, '', raw_html)
            text_string = ''.join(clean_text)
            wc = WordCloud(max_font_size=200, font_path='C:\\Windows\\Fonts\\batang.ttc', background_color='white', height=230).generate(text_string)
            img_path = f'{settings.MEDIA_ROOT}/visual/{self.request.user.username}_wordcloud.jpg'
            html_path = f'/media/visual/{self.request.user.username}_wordcloud.jpg'
            wc.to_file(img_path)
        
        
        return render(self.request, 'profileapp/visualize.html', {'content':html_path, 'data':data, 'amount':len(diary_list)})