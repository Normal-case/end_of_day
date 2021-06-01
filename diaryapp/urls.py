from django.urls import path
from .views import *

app_name = 'diaryapp'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/<int:year>/<int:month>/<int:day>/', DiaryCreate.as_view(), name='create'),
    path('create/common/<int:year>/<int:month>/<int:day>/', DiaryCreateCommon.as_view(), name='create_common'),
    path('create/select/<int:year>/<int:month>/<int:day>/', DiarySelectFeeling.as_view(), name='select_feeling'),
    path('create/select/who/<int:pk>', DiarySelectWho.as_view(), name='select_who'),
    path('create/select/when/<int:pk>', DiarySelectWhen.as_view(), name='select_when'),
    path('create/select/where/<int:pk>', DiarySelectWhere.as_view(), name='select_where'),
    path('create/select/what/<int:pk>', DiarySelectWhat.as_view(), name='select_what'),
    path('create/select/how/<int:pk>', DiarySelectHow.as_view(), name='select_how'),
    path('create/select/why/<int:pk>', DiarySelectWhy.as_view(), name='select_why'),
    path('create/select/continue/<int:pk>', DiarySelectContinue.as_view(), name='select_continue'),
    path('read/<int:pk>', DiaryRead.as_view(), name='read'),
    path('update/<int:pk>', DiaryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DiaryDeleteView.as_view(), name='delete'),
]