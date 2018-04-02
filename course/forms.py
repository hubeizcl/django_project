from django import forms
from .models import Course, Lession


class CreatedCoureForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'overview',)


class CreatedLessonForm(forms.ModelForm):
    class Meta:
        model = Lession
        fields = ['course', 'title', 'video', 'description', 'attach']

    def __init__(self, user, *args, **kwargs):
        super(CreatedLessonForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)
