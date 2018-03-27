from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn


# Create your views here.

@login_required(login_url='/account/login/')
def article_column(request):
    columns = ArticleColumn.objects.filter(user=request.user)  # 根据当前用户筛选出和当前用户一直的文章的元组
    return render(request, 'article/column/article_column.html', {"columns": columns})
