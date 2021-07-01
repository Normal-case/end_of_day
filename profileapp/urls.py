from django.urls import path
from profileapp.views import *

app_name = 'profileapp'
urlpatterns = [
    path('<str:id>/', ProfileMain.as_view(), name='main'),
    path('create/<str:id>/', ProfileCreate.as_view(), name='create'),
    path('visual/<str:id>/', Visualize.as_view(), name='visual'),
]