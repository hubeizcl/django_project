from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn, ArticlePost
from .form import ArticleColumnForm, ArticlePostForm
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


@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)  # 获取表单数据
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)  # 将表单对象转换成实体对象，暂时不提交数据库
                new_article.author = request.user  # 将当前用户对象赋值给实体对象
                new_article.column = request.user.article_column.get(
                    id=request.POST['column_id'])  # 通过外键将column对象赋值给实体对象
                new_article.save()
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html",
                      {"article_post_form": article_post_form, "article_columns": article_columns})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request, "article/column/article_list.html", {"articles": articles})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


@login_required(login_url='/account/login/')
@csrf_exempt
def rename_article(request):
    article_name = request.POST['article_name']
    article_id = request.POST['article_id']
    try:
        line = ArticlePost.objects.get(id=article_id)
        line.column = article_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@login_required(login_url='/account/login/')
@csrf_exempt
def delete_article(request):
    article_id = request.POST['article_id']
    try:
        line = ArticlePost.objects.get(id=article_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')
