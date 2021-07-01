from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import CrossDiaryContent
from profileapp.models import Profile

def account_ownership_nickname(func):
    def decorated(request, *args, **kwargs):
        user_a = Profile.objects.get(nickname=kwargs['user_a'])
        user_b = Profile.objects.get(nickname=kwargs['user_b'])
        if (not user_a.nickname == request.user.profile.nickname) and (not user_b.nickname== request.user.profile.nickname):
            return HttpResponseForbidden("<div style='text-align: center;'><img src='/static/warning.png' style='width: 200px;' alt=''><p>잘못된 접근입니다.</p></div>")
        return func(request, *args, **kwargs)
    return decorated

def account_ownership_crossdiarykey(func):
    def decorated(request, *args, **kwargs):
        content = CrossDiaryContent.objects.get(pk=kwargs['pk'])
        if (not content.cross.user_a == request.user.profile.nickname) and (not content.cross.user_b == request.user.profile.nickname):
            return HttpResponseForbidden("<div style='text-align: center;'><img src='/static/warning.png' style='width: 200px;' alt=''><p style='font-size: 24px;'>잘못된 접근입니다.</p></div>")
        return func(request, *args, **kwargs)
    return decorated