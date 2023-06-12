from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, RegisterForm, NewsAddForm
from .models import News, User
from django.core.paginator import Paginator
from django.contrib import messages


def main(request):
    searched = request.GET.get('search_word')
    # all_news = []
    if searched:
        all_news = News.objects.filter(title__contains=searched)
    else:
        all_news = News.objects.all()

    paginator = Paginator(all_news, 6)
    page_num = request.GET.get('page', 6)
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
    searched = request.GET.get('search_word')
    if searched:
        news_list = News.objects.filter(category_id=category_id, title__contains=searched)
    else:
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


@login_required
def add_news(request):
    if request.method == 'GET':
        form = NewsAddForm()
        return render(request, 'news/news_add.html', {'form': form})

    if request.method == 'POST':
        form = NewsAddForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.publisher = request.user
            news.save()
            messages.success(request, 'News added successfully.')
            return redirect('main')
        else:
            messages.error(request, 'Something went wrong')
            return render(request, 'news/news_add.html', {'form': form})


@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_data = {
        'user': user
    }
    return render(request, 'news/profile.html', context=user_data)


def my_news(request):
    searched = request.GET.get('search_word')
    if searched:
        publisher_news = News.objects.filter(publisher=request.user, title__contains=searched)
    else:
        publisher_news = News.objects.filter(publisher=request.user)

    paginator = Paginator(publisher_news, 6)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'page_obj': page_objects
    }

    return render(request, 'news/index.html', context=context)


def update_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        avatar = request.FILES.get('picture')

        # Update the user's profile data
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.avatar = avatar
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile', user_id=request.user.id)

    return render(request, 'news/update_profile.html')


def publishers(request):
    all_publishers = User.objects.all()
    context = {
        'all_publishers': all_publishers,
    }
    return render(request, 'news/publishers.html', context=context)


def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.media = request.FILES.get('picture')
        news.save()

        return redirect('details', news.id)

    context = {
        'news': news
    }

    return render(request, 'news/edit_news.html', context=context)
