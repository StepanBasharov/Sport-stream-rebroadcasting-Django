from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import *
from django.views import View
from django.contrib.auth.views import LoginView
from datetime import datetime, timedelta
from .forms import *


def translation_filter(request, template):
    # Получаем 3 возможных запроса
    category_key = request.POST.get('sport')
    day = request.POST.get('day')
    calendar = request.POST.get('calendar')
    category_news = request.POST.get('news_filter')
    login = LoginForm()

    global data_date
    # Проверяем, по какой форме пользователь проводил фильтрацию
    if category_key != None or day != None or calendar != None or category_news != None:
        news = News.objects.all()
        news_key = 'all'
        if category_news != None:
            category = Category.objects.all()
            translations = Translation.objects.all()
            if category_news == "all":
                news = News.objects.all()
            else:
                news = News.objects.filter(category__name=category_news)
            news_key = category_news
            first_news = news[:3]
            news = news[3:]
            return render(request, template,
                          {"category": category, "translations": translations, 'news': news,
                           'first_news': first_news,
                           'key': 'all',
                           "news_key": news_key, 'day': 'Сегодня',
                           'is_filter': False, 'login_form': login})
        else:
            # Проверяем, по какому запросы пришли валидные данные
            try:
                category = category_key.split("_")[1]
                date = category_key.split("_")[0]
            except Exception:
                try:
                    category = day.split("_")[1]
                    date = day.split("_")[0]
                except Exception:
                    try:
                        category = calendar.split("_")[1]
                        data_date = calendar.split("_")[0]
                        date = ".".join(data_date.split("-")[::-1])
                    except Exception:
                        pass

            # Переводим буквенную дату в формат python
            date_format = '%Y-%m-%d'
            today = datetime.now()
            filter_time = None
            if date == 'Сегодня':
                filter_time = today
            elif date == "Вчера":
                filter_time = today - timedelta(days=1)
            elif date == "Завтра":
                filter_time = today + timedelta(days=1)
            else:
                date_filter = data_date
            if filter_time:
                date_filter = filter_time.strftime(date_format)

            category_list = Category.objects.all()
            translations = Translation.objects.all()
            first_news = news[:3]
            news = news[3:]

            if category == "all":
                filtered_translations = Translation.objects.filter(
                    date=date_filter)
            else:
                filtered_translations = Translation.objects.filter(
                    category__name=category, date=date_filter)
            if request.build_absolute_uri().split('/')[-2] == "translation":
                data = Translation.objects.get(id=request.build_absolute_uri().split('/')[-1])
                data_key = "translation_data"
            elif request.build_absolute_uri().split('/')[-2] == "news":
                data = News.objects.get(id=request.build_absolute_uri().split('/')[-1])
                data_key = "news_data"
            else:
                data = None
                data_key = ''
            return render(request, template,
                          {data_key: data, "category": category_list, "translations": translations, 'news': news,
                           'first_news': first_news,
                           'filtered_translations': filtered_translations, 'key': category, 'day': date,
                           "day_date": date_filter, 'is_filter': True, "news_key": news_key, 'login_form': login})
    # Если POST запрос прошел по некорректной форме
    else:
        category = Category.objects.all()
        translations = Translation.objects.all()
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        return render(request, template,
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login})


class Login(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                print(1)
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            return HttpResponse('Invalid Form')


class Index(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        translations = Translation.objects.all()
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        login = LoginForm()
        return render(request, 'index.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'index.html')


class TranslationPage(View):
    def get(self, request, pk, *args, **kwargs):
        data = Translation.objects.get(id=pk)
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'translationcard.html',
                      {'translation_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'translationcard.html')


class NewsPage(View):
    def get(self, request, pk, *args, **kwargs):
        data = News.objects.get(id=pk)
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'newscard.html',
                      {'news_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'newscard.html')


class NewsList(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'news.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'news.html')


class TranslationsList(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'translationslist.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'translationslist.html')


class SubPage(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'subscription.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'subscription.html')
