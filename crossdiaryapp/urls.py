from crossdiaryapp.models import CrossDiaryContent
from django.urls import path
from .views import *

app_name = 'crossdiaryapp'
urlpatterns = [
    path('<str:id>/', CrossDiaryList.as_view(), name='list'),
    path('<str:user_a>/<str:user_b>/', HomeView.as_view(), name='home'),
    path('create/<int:year>/<int:month>/<int:day>/<str:user_a>/<str:user_b>/', CrossDiaryCreate.as_view(), name='create'),
    path('create/common/<int:year>/<int:month>/<int:day>/<str:user_a>/<str:user_b>/', CrossDiaryCreateCommon.as_view(), name='create_common'),
    path('create/select/<int:year>/<int:month>/<int:day>/<str:user_a>/<str:user_b>/', CrossDiarySelectFeeling.as_view(), name='select_feeling'),
    # crossdiarycontent.pk
    path('create/select/who/<int:pk>', CrossDiarySelectWho.as_view(), name='select_who'),
    path('create/select/when/<int:pk>', CrossDiarySelectWhen.as_view(), name='select_when'),
    path('create/select/where/<int:pk>', CrossDiarySelectWhere.as_view(), name='select_where'),
    path('create/select/what/<int:pk>', CrossDiarySelectWhat.as_view(), name='select_what'),
    path('create/select/how/<int:pk>', CrossDiarySelectHow.as_view(), name='select_how'),
    path('create/select/why/<int:pk>', CrossDiarySelectWhy.as_view(), name='select_why'),
    path('create/select/continue/<int:pk>', CrossDiarySelectContinue.as_view(), name='select_continue'),
    path('read/<int:pk>', CrossDiaryRead.as_view(), name='read'),
    path('update/<int:pk>', CrossDiaryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', CrossDiaryDeleteView.as_view(), name='delete'),
]