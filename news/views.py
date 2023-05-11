from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm
from .models import News
from django.core.paginator import Paginator
from django.contrib import messages


def main(request):
    searched = request.GET.get('search_word')
    # all_news = []
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


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'news/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('main')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'news/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, f'You have been successfully logged out')
    return redirect('login')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'news/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request)
            return redirect('main')
        else:
            return render(request, 'news/register.html', {'form': form})
