#encoding: utf-8
from django.urls import path
from . import views

app_name = 'cms'


urlpatterns = [
    path('cms_index/',views.cms_index,name='cms_index'),
    path('article_category/',views.article_category,name='article_category'),
    path('add_article_category/',views.add_acticle_category,name='add_article_category'),
    path('edit_article_category/',views.edit_article_category,name='edit_article_category'),
    path('delete_article_category/',views.delete_article_category,name='delete_article_category'),
    path('write_news/',views.WriteArticle.as_view(),name='write_news'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('article_list/',views.ArticleListView.as_view(),name='article_list'),
    path('edit_list/',views.EditArticleView.as_view(),name='edit_list'),
    path('delete_article/',views.delete_article,name='delete_article'),
]