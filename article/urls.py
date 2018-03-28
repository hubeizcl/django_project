from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article_column/$', views.article_column, name="article_column"),
    url(r'^rename_article_column/$', views.rename_article_column, name="rename_article_column"),
    url(r'^delete_article_column/$', views.delete_article_column, name="delete_article_column"),
    url(r'^article_post/$', views.article_post, name="article_post"),
    url(r'^article_list/$', views.article_list, name="article_list"),
    url(r'^article_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
    url(r'^rename_article/$', views.rename_article, name="rename_article"),
    url(r'^delete_article/$', views.delete_article, name="delete_article"),
]
app_name = 'article'
