from django.urls import path
from . import views

app_name = 'videocourse'

urlpatterns = [
    path('video_index/', views.video_index, name='video_index'),
]