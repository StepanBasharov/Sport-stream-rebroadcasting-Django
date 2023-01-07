from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import *
from django.views import View
from django.contrib.auth.views import LoginView
from datetime import datetime, timedelta
from .forms import *

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .token import account_activation_token


def translation_filter(request, template):
    # Получаем 3 возможных запроса
    category_key = request.POST.get('sport')
    day = request.POST.get('day')
    calendar = request.POST.get('calendar')
    category_news = request.POST.get('news_filter')
    login_form = LoginForm()
    register = UserRegistrationForm()

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
                           'is_filter': False, 'login_form': login_form, 'reg_form': register})
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
                           "day_date": date_filter, 'is_filter': True, "news_key": news_key, 'login_form': login_form,
                           'reg_form': register})
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
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})


def activate_mail(request, user, email):
    print("Test Go 3")
    mail_subject = 'Активируйте аккаунт для доступа к контенту.'
    message = render_to_string('email_activate.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    print("Test Go 4")
    email.send()
    print("Test Go5")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')

    else:
        login_form = LoginForm()
        reg_form = UserRegistrationForm()
        return render(request, 'reg-trabl.html',
                      {'login_form': login_form, 'reg_form': reg_form, 'message': "Неккоректная ссылка."})

    return redirect('index')


class Login(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    login_form = LoginForm()
                    reg_form = UserRegistrationForm()
                    return render(request, 'reg-trabl.html',
                                  {'login_form': login_form, 'reg_form': reg_form, 'message': "Ваш аккаунт отключен"})
            else:
                login_form = LoginForm()
                reg_form = UserRegistrationForm()
                return render(request, 'reg-trabl.html',
                              {'login_form': login_form, 'reg_form': reg_form,
                               'message': "Такого пользователя не существует"})
        else:
            return HttpResponse('500')


class Register(View):
    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            cd = user_form.cleaned_data
            print("Test Go 1")
            activate_mail(request, new_user, cd['email'])
            # user = authenticate(username=cd['username'], password=cd['password'])
            # login(request, user)
            print("Test Go 2")
            login_form = LoginForm()
            register = UserRegistrationForm()
            return render(request, 'reg-trabl.html', {
                'message': f'Дорогой {cd["username"]}! Вам нужно подтвердить вашу почту, пожалуйста, проверьте почтовый ящик {cd["email"]}',
                'login_form': login_form, 'reg_form': register})
        else:
            login_form = LoginForm()
            reg_form = UserRegistrationForm()
            return render(request, 'reg-trabl.html',
                          {'login_form': login_form, 'reg_form': reg_form, 'message': "Введены неккоректные данные"})


class Index(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        translations = Translation.objects.all()
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'index.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'index.html')


class TranslationPage(View):
    def get(self, request, pk, *args, **kwargs):
        data = Translation.objects.get(id=pk)
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'translationcard.html',
                      {'translation_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'translationcard.html')


class NewsPage(View):
    def get(self, request, pk, *args, **kwargs):
        data = News.objects.get(id=pk)
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'newscard.html',
                      {'news_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'newscard.html')


class NewsList(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'news.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'news.html')


class TranslationsList(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'translationslist.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'translationslist.html')


class SubPage(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'subscription.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'subscription.html')
