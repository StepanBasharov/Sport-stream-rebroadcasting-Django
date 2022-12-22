from django.shortcuts import render
from .models import Category, Translation
from django.views import View
from datetime import datetime, timedelta


class Index(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        translations = Translation.objects.all()
        return render(request, 'index.html',
                      {"category": category, "translations": translations, 'key': 'all', 'day': 'Сегодня'})

    def post(self, request, *args, **kwargs):
        # Получаем 3 возможных запроса
        category_key = request.POST.get('sport')
        day = request.POST.get('day')
        calendary = request.POST.get('calendar')
        global data_date
        # Нужно для нормально изменения данных
        # Проверяем по какому запросы пришли валидные данные
        try:
            category = category_key.split("_")[1]
            date = category_key.split("_")[0]
        except Exception:
            try:
                category = day.split("_")[1]
                date = day.split("_")[0]
            except Exception:
                category = calendary.split("_")[1]
                data_date = calendary.split("_")[0]
                date = ".".join(data_date.split("-")[::-1])
        # Переводим слова в нормальную дату для фильтрации трансляций
        if date == 'Сегодня':
            date_format = '%Y-%m-%d'
            today = datetime.now()
            date_filter = today.strftime(date_format)
        elif date == "Вчера":
            date_format = '%Y-%m-%d'
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            date_filter = yesterday.strftime(date_format)
        elif date == "Завтра":
            date_format = '%Y-%m-%d'
            today = datetime.now()
            tomorrow = today + timedelta(days=1)
            date_filter = tomorrow.strftime(date_format)
        else:
            date_filter = data_date
        category_list = Category.objects.all()
        translations = Translation.objects.all()
        if category == "all":
            filtered_translations = Translation.objects.filter(date=date_filter)
        else:
            filtered_translations = Translation.objects.filter(category__name=category, date=date_filter)
        return render(request, 'filtred_translations.html',
                      {"category": category_list, "translations": translations,
                       'filtered_translations': filtered_translations, 'key': category, 'day': date,
                       "day_date": date_filter})
