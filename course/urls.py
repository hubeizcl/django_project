from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'course'
urlpatterns = [
    url('^about/$', TemplateView.as_view(template_name='course/about.html'), name='about'),
    url('^course_list/$', views.CourseListView.as_view(), name='course_list'),
    url('^course_manage/$', views.ManageCourseListView.as_view(), name='course_manage'),
    url('^course_created/$', views.CreatedCourseView.as_view(), name='course_created'),
    url('^course_delete/(?P<pk>\d+)/$', views.DeleteCourseView.as_view(), name='course_delete'),
    url('^lesson_created/$', views.CreatedLessionView.as_view(), name='lesson_created'),
    url('^list_lesson/(?P<course_id>\d+)/$', views.ListLessonsView.as_view(), name='list_lesson'),
    url('^detail_lesson/(?P<lesson_id>\d+)/$', views.DetailLessonview.as_view(), name='detail_lesson'),
]
