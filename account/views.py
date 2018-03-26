from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Userinfo, UserProfile


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
            Userinfo.objects.create(user=new_user)
            return HttpResponse('successfully')
        else:
            return HttpResponse('sorry,you can not register')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile': userprofile_form})


@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = Userinfo.objects.get(user=user)
    return render(request, 'account/myself_information.html',
                  {"user": user, "userprofile": userprofile, "userinfo": userinfo})


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = Userinfo.objects.get(user=user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid() and userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.brith = userprofile_cd['brith']
            userprofile.phone = userprofile_cd['phone']
            userinfo.company = userinfo_cd['company']
            userinfo.school = userinfo_cd['school']
            userinfo.address = userinfo_cd['address']
            userinfo.profession = userinfo_cd['profession']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
            return HttpResponseRedirect('account/my_information')
        else:
            user_form = UserForm(instance=request.user)
            userprofile_form = UserProfileForm(initial={"brith": userprofile.brith, "phone": userprofile.phone})
            userinfo_form = UserInfoForm(
                initial={"school": userinfo.school, "company": userinfo.company, "address": userinfo.address,
                         "profession": userinfo.profession, "aboutme": userinfo.aboutme})
            return render(request, 'account/edit_myself_information.html',
                          {"user": user_form, "userprofile": userprofile_form, "userinfo": userinfo_form})
