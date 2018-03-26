from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm


# Create your views here.
def user_login(request):
    if request.method == "POST":  # 根据请求方式做后续操作
        login_form = LoginForm(request.POST)  # 获取POST请求发送过来的参数，并将其赋值给LoginForm对象
        if login_form.is_valid():  # 对传入的参数做校验
            cd = login_form.cleaned_data  # 读取表单数据，转换成字典类型
            user = authenticate(username=cd['username'], password=cd['password'])  # 提取数据进行验证，底层应该是将两个值放入SQL语句中然后到数据库查询
            if user:
                login(request, user)  # 将读取的user对象放入session中
                return HttpResponse('welcome ,you username and password is right.')
            else:
                return HttpResponse('sorry ,you username and password is not right.')
        else:
            return HttpResponse('invalid login')
    if request.method == "GET":
        login_form = LoginForm()  # 创建一个空对象
        return render(request, 'account/login.html', {"form": login_form})  # 返回一个登陆界面


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse('successfully')
        else:
            return HttpResponse('sorry,you can not register')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile': userprofile_form})
