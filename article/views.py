from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from .form import ArticleColumnForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)  # 根据当前用户筛选出和当前用户一直的文章的元组
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html', {"columns": columns, "column_form": column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@login_required(login_url='/account/login/')
@csrf_exempt
def delete_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')
