from asyncio import sleep

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import *
from django.views import View
from django.contrib.auth.views import LoginView
from datetime import datetime, timedelta, date
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
    mail_subject = 'Активируйте аккаунт для доступа к контенту.'
    message = render_to_string('email_activate.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    email.send()


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
        sub = Subscription.objects.get(sub_name='Базовая')
        new_sub = UserSubs(
            user=user,
            sub=sub
        )
        new_sub.save()
        login(request, user)
        return redirect('index')

    else:
        login_form = LoginForm()
        reg_form = UserRegistrationForm()
        return render(request, 'reg-trabl.html',
                      {'login_form': login_form, 'reg_form': reg_form, 'message': "Неккоректная ссылка."})

    return redirect('index')


def rename(request):
    if request.method == "POST":
        new_name = request.POST.get('username')
        user = User.objects.get(username=request.user)
        user.username = new_name
        user.save()
        return redirect('profile')
    else:
        return redirect('profile')


def new_mail(request):
    if request.method == "POST":
        new_email = request.POST.get('email')
        user = User.objects.get(username=request.user)
        user.email = new_email
        user.save()
        return redirect('profile')
    else:
        return redirect('profile')


def set_new_password(request):
    if request.method == "POST":
        user = request.user
        if len(request.POST['password']) < 5:
            return redirect('profile')
        user.set_password(request.POST['password'])
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return redirect('profile')


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
            login_form = LoginForm()
            register = UserRegistrationForm()
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            cd = user_form.cleaned_data
            if cd['email'] in User.objects.filter(is_active=True).values_list('email', flat=True):
                return render(request, 'reg-trabl.html', {
                    'message': f'Дорогой {cd["username"]}! Почта {cd["email"]} уже используется другим пользователем!',
                    'login_form': login_form, 'reg_form': register})
            activate_mail(request, new_user, cd['email'])
            login_form = LoginForm()
            register = UserRegistrationForm()
            return render(request, 'reg-trabl.html', {
                'message': f'Дорогой {cd["username"]}! Вам нужно подтвердить вашу почту, пожалуйста, проверьте почтовый ящик {cd["email"]}',
                'login_form': login_form, 'reg_form': register})
        else:
            login_form = LoginForm()
            reg_form = UserRegistrationForm()
            return render(request, 'reg-trabl.html',
                          {'login_form': login_form, 'reg_form': reg_form,
                           'message': "Введены неккоректные данные\n(Бранные слова, Совпадение пароля и логина, Совпадени пароля и почты)"})


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
        comments = TranslationComment.objects.filter(translation__name=data.name)
        category = Category.objects.all()
        user_data = UserSubs.objects.get(user=request.user)
        translations = Translation.objects.all()
        login_form = LoginForm()
        sub_end_date = user_data.end_sub
        end_sub = False
        if sub_end_date == None:
            end_sub = True
        else:
            if date.today() > sub_end_date:
                end_sub = True
        register = UserRegistrationForm()
        if_ultimate = str(user_data.sub)
        return render(request, 'translationcard.html',
                      {'translation_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register, 'comments': comments,
                       'user_data': user_data, 'if_ultimate': if_ultimate, 'end_sub': end_sub, 'pk': pk})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'translationcard.html')


class NewsPage(View):
    def get(self, request, pk, *args, **kwargs):
        data = News.objects.get(id=pk)
        comments = NewsComment.objects.filter(news__name=data.name)
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        return render(request, 'newscard.html',
                      {'news_data': data, "category": category, "translations": translations,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register, 'comments': comments})

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
        subs = Subscription.objects.all()
        register = UserRegistrationForm()
        return render(request, 'subscription.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False, 'login_form': login_form, 'reg_form': register, 'subs': subs})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'subscription.html')


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            post = News.objects.get(pk=pk)

            is_dislike = False

            for dislike in post.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if is_dislike:
                post.dislikes.remove(request.user)

            is_like = False

            for like in post.likes.all():
                if like == request.user:
                    is_like = True
                    break

            if not is_like:
                post.likes.add(request.user)

            if is_like:
                post.likes.remove(request.user)

            return HttpResponseRedirect(reverse('news_card', args=[str(pk)]))
        else:
            return redirect('news_list')


class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            post = News.objects.get(pk=pk)

            is_like = False

            for like in post.likes.all():
                if like == request.user:
                    is_like = True
                    break

            if is_like:
                post.likes.remove(request.user)

            is_dislike = False

            for dislike in post.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if not is_dislike:
                post.dislikes.add(request.user)

            if is_dislike:
                post.dislikes.remove(request.user)

            return HttpResponseRedirect(reverse('news_card', args=[str(pk)]))
        else:
            return redirect('news_list')


class NewNewsComment(View):
    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            comment = request.POST.get('comment')
            obscene_words = [
                'хуй',
                'пизда',
                'уебок',
                'ебать',
                'выеб',
                'выёб',
            ]
            for word in obscene_words:
                if word in comment.lower():
                    return HttpResponseRedirect(reverse('news_card', args=[str(pk)]))
            new_comment = NewsComment(
                author=request.user,
                text=comment,
                news=News.objects.get(pk=pk)
            )
            new_comment.save()
            return HttpResponseRedirect(reverse('news_card', args=[str(pk)]))


class NewTranslationComment(View):
    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            comment = request.POST.get('comment')
            obscene_words = [
                'хуй',
                'пизда',
                'уебок',
                'ебать',
                'выеб',
                'выёб',
            ]
            for word in obscene_words:
                if word in comment.lower():
                    return HttpResponseRedirect(reverse('translation', args=[str(pk)]))
            new_comment = TranslationComment(
                author=request.user,
                text=comment,
                translation=Translation.objects.get(pk=pk)
            )
            new_comment.save()
            return HttpResponseRedirect(reverse('translation', args=[str(pk)]))


class UserProfile(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        category = Category.objects.all()
        translations = Translation.objects.all()
        login_form = LoginForm()
        register = UserRegistrationForm()
        if request.user.is_authenticated:
            subscription = UserSubs.objects.get(user=request.user)
            subscription = subscription.sub
            return render(request, 'settings.html',
                          {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                           'key': 'all',
                           "news_key": 'all', 'day': 'Сегодня',
                           'is_filter': False, 'login_form': login_form, 'reg_form': register, 'subs': subscription})
        else:
            return render(request, 'settings.html',
                          {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                           'key': 'all',
                           "news_key": 'all', 'day': 'Сегодня',
                           'is_filter': False, 'login_form': login_form, 'reg_form': register})

    def post(self, request, *args, **kwargs):
        return translation_filter(request, 'settings.html')
