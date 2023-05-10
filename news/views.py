from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .models import News, Category
from django.core.paginator import Paginator


def main(request):
    searched = request.GET.get('search_word')
    all_news = []
    if searched:
        all_news = News.objects.filter(title__contains=searched)
    else:
        all_news = News.objects.all()

    paginator = Paginator(all_news, 1)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'all_news': all_news,
        'page_obj': page_objects
    }

    return render(request, 'news/index.html', context=context)


def details(request, news_id):
    news = News.objects.get(id=news_id)
    context = {
        'news': news,
    }
    return render(request, 'news/details.html', context=context)


def category(request, category_id):
    news_list = News.objects.filter(category_id=category_id)
    data = {
        'news_list': news_list,
    }
    return render(request, 'news/category.html', context=data)
