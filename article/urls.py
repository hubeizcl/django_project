from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article_column/$', views.article_column, name="article_column"),
    url(r'^rename_article_column/$', views.rename_article_column, name="rename_article_column"),
    url(r'^delete_article_column/$', views.delete_article_column, name="delete_article_column"), ]
app_name = 'article'
