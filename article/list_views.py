from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import redis
from django.conf import settings
from .form import CommentForm
from django.db.models import Count

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
    total_views = r.incr("article:{}:views".format(article.id))  # 在Redis中存入键为article:1:views值为自增数值的键值对
    r.zincrby('article_ranking', article.id, 1)  # 隐藏含义就是，没有就创建一个有序的zset集合，然后在其中存入以article.id为主键，初始值为零，步增为1的一个集合

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True, withscores=False)[
                      :10]  # 拿到article_ranking这个zset所有根据倒序排列的一个列表，然后取前十位
    article_ranking_ids = []  # 获取上述列表的所有的id值，将其转换成数值列表
    for id in article_ranking:
        try:
            article_ranking_ids.append(int(id))
        except ValueError:
            continue
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))  # 根据这些ID值拿到对应的article，并将其塞入列表中
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    global similar_articles
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
        article_tags_ids = article.article_tag.values_list('id', flat=True)
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')[
                           :4]
    return render(request, "article/list/article_detail.html",
                  {"article": article, "total_views": total_views, "most_viewed": most_viewed,
                   "comment_form": comment_form, "similar_articles": similar_articles})


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
