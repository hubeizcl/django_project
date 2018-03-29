from django import template
from django.db.models import Count

register = template.Library()
from article.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_article(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {"latest_articles": latest_articles}


@register.inclusion_tag('article/list/most_commented_articles.html')
def most_commented_articles(n=3):
    most_commented_articles = ArticlePost.objects.annotate(total_comments=Count('comments')).order_by(
        "-total_comments")[:n]
    return {"most_commented_articles": most_commented_articles}
