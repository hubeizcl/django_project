from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Userinfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    # username = forms.CharField(label="username", widget=forms.TextInput)
    # email = forms.CharField(label="email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm Password", widget=forms.PasswordInput)

    class Meta:
        model: User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password do not match')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'brith')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Userinfo
        fields = ("school", "company", "profession", "address", "aboutme")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
