from django.urls import path, re_path
from . import views

app_name = 'dictationTool'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^dictationTool/$', views.dictationTool, name='dictationTool'),
]
