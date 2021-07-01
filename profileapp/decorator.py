from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

def account_ownership_username(func):
    def decorated(request, *args, **kwargs):
        user = User.objects.get(username=kwargs['id'])
        if not user == request.user:
            return HttpResponseForbidden("<div style='text-align: center;'><img src='/static/warning.png' style='width: 200px;' alt=''><p>잘못된 접근입니다.</p></div>")
        return func(request, *args, **kwargs)
    return decorated