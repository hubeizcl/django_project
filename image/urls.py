from django.conf.urls import url
from image import views

urlpatterns = [
    url(r'^list_images/$', views.list_image, name="list_images"),
    url(r'^upload_image/$', views.upload_image, name="upload_image"),
]
app_name = 'image'
