from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article_column/$', views.article_column, name="article_column"),
]
app_name = 'article'
