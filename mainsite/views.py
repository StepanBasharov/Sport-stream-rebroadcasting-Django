from django.shortcuts import render
from .models import *
from django.views import View
from datetime import datetime, timedelta


class Index(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        translations = Translation.objects.all()
        news = News.objects.all()
        first_news = news[:3]
        news = news[3:]
        return render(request, 'index.html',
                      {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                       'key': 'all',
                       "news_key": 'all', 'day': 'Сегодня',
                       'is_filter': False})

    def post(self, request, *args, **kwargs):
        # Получаем 3 возможных запроса
        category_key = request.POST.get('sport')
        day = request.POST.get('day')
        calendar = request.POST.get('calendar')

        global data_date
        # Проверяем, по какой форме пользователь проводил фильтрацию
        if category_key != None or day != None or calendar != None:
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
            news = News.objects.all()
            first_news = news[:3]
            news = news[3:]

            if category == "all":
                filtered_translations = Translation.objects.filter(
                    date=date_filter)
            else:
                filtered_translations = Translation.objects.filter(
                    category__name=category, date=date_filter)
            return render(request, 'index.html',
                          {"category": category_list, "translations": translations, 'news': news,
                           'first_news': first_news,
                           'filtered_translations': filtered_translations, 'key': category, 'day': date,
                           "day_date": date_filter, 'is_filter': True})
        # Если POST запрос прошел по некорректной форме
        else:
            category = Category.objects.all()
            translations = Translation.objects.all()
            news = News.objects.all()
            first_news = news[:3]
            news = news[3:]
            return render(request, 'index.html',
                          {"category": category, "translations": translations, 'news': news, 'first_news': first_news,
                           'key': 'all',
                           "news_key": 'all', 'day': 'Сегодня',
                           'is_filter': False})
