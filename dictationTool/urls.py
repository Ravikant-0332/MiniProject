from django.urls import path
from . import views

app_name = 'dictationTool'

urlpatterns = [
    path('', views.home, name='home'),
    path('dictationTool/', views.dictationTool, name='dictationTool'),
]
