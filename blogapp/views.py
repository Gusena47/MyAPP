from django.shortcuts import render
from django.views.generic import ListView
from .models import Article


# Create your views here.
class ArticleListView(ListView):
    template_name = '/blogapp/article_list.html'
    model = Article

    queryset = (
        Article.objects
        .select_related("author")
        .select_related("category")
        .prefetch_related('tags')
        .defer('content')
    )