from django.conf.urls import url
from image import views

urlpatterns = [
    url(r'^list_images/$', views.list_image, name="list_images"),
    url(r'^upload_image/$', views.upload_image, name="upload_image"),
    url(r'^del_image/$', views.del_image, name="del_image"),
    url(r'^falls_images/$', views.falls_images, name="falls_images"),
]
app_name = 'image'
