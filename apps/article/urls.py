#encoding: utf-8
from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('<int:article_id>/',views.article_detail,name='article_detail'),
    path('login/',views.logon_view,name='login'),
    path('lognup/',views.lognup_view,name='lognup'),
    path('article_list/',views.article_list,name='article_list'),
    path('public_comment/',views.public_comment,name='public_comment'),

]