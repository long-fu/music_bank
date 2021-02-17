from django.shortcuts import render
from django.views import generic
from .models import File,Audio
# Create your views here.
# 前端 数据显示
class IndexView(generic.ListView):
    template_name  = 'bee/index.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        return File.objects.all() 
    pass

class AudioIndexView(generic.ListView):
    template_name  = 'bee/audio.html'
    context_object_name = 'list'
    def get_queryset(self):
        return Audio.objects.all() 
    pass