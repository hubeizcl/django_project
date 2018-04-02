from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.views.generic.base import TemplateResponseMixin
from .models import Course, Lession
from django.contrib.auth.models import User
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, LoginRequiredMixin
from .forms import CreatedCoureForm, CreatedLessonForm
from django.urls import reverse_lazy
import json
from django.views import View


# Create your views here.
class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = '/account/login/'


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = 'courses'
    template_name = 'course/manage/manage_course_list.html'


class Fooview(CsrfExemptMixin, JsonRequestResponseMixin):
    def post(self, request, *args, **kwargs):
        data = {'name': 'xiaoshi', 'web': 'django'}
        return self.render_json_response(data)


class CreatedCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']
    template_name = 'course/manage/created_course.html'

    def post(self, request, *args, **kwargs):
        form = CreatedCoureForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect('course:course_manage')
        return self.render_to_response({'form': form})


class DeleteCourseView(UserCourseMixin, DeleteView):
    # template_name = 'course/manage/course_confirm_delete.html'
    success_url = reverse_lazy('course:course_manage')

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return resp


class CreatedLessionView(LoginRequiredMixin, View):
    model = Lession
    login_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        form = CreatedLessonForm(user=self.request.user)
        return render(request, 'course/manage/created_lession.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreatedLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect('course:course_manage')


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = '/account/login/'
    template_name = 'course/manage/list_lessons.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course': course})


class DetailLessonview(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = '/account/login/'
    template_name = 'course/manage/detail_lesson.html'

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lession, id=lesson_id)
        return self.render_to_response({"lesson": lesson})
