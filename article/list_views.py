from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all();
    paginator = Paginator(article_title, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, 'article/list/author_article.html',
                      {"articles": articles, "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, 'article/list/article_title.html', {"articles": articles, "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/list/article_detail.html", {"article": article})


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == 'like':
                article.user_like.add(request.user)
                return HttpResponse('1')
            else:
                article.user_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse('no')