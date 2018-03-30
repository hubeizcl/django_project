from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn, ArticlePost, ArticleTag
from .form import ArticleColumnForm, ArticlePostForm, ArticleTagForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


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
                tags = request.POST['tags']
                print(tags)
                if tags:
                    for tag in json.loads(tags):
                        tag = request.user.tag.get(tag=tag)
                        new_article.article_tag.add(tag)
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_tags = request.user.tag.all()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html",
                      {"article_post_form": article_post_form, "article_columns": article_columns,
                       "article_tags": article_tags})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = Paginator.page(self=paginator, number=1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


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


@login_required(login_url='/account/login/')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()  # 获取当前用户的所有columns
        article = ArticlePost.objects.get(id=article_id)  # 获取当前需要修改的article
        this_article_form = ArticlePostForm(initial={"title": article.title})  # 获取当前获取当前需要修改的article主题的input对象
        this_article_column = article.column  # 获取column的input对象
        return render(request, 'article/column/redit_article.html',
                      {"article": article, "article_columns": article_columns, "this_article_form": this_article_form,
                       "this_article_column": this_article_column})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required(login_url='/account/login/')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tag = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, 'article/tag/tag_list.html',
                      {"article_tag_form": article_tag_form, "article_tag": article_tag})
    if request.method == "POST":
        article_tag_form = ArticleTagForm(data=request.POST)
        if article_tag_form.is_valid():
            try:
                new_tag = article_tag_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse('1')
            except:
                return HttpResponse('the data cannot be save')
        else:
            return HttpResponse('sorry,the form is not valid')


@login_required(login_url='/account/login/')
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['id']
    try:
        article_tag = ArticleTag.objects.filter(id=tag_id)
        article_tag.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')
