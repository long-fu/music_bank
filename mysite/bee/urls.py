from django.urls import path,re_path,include
from . import views

app_name = 'bee'

urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('audio', views.AudioIndexView.as_view()),
]
