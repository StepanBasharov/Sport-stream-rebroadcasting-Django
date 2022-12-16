from django.shortcuts import render
from .models import Category, Translation


def index(request):
    category = Category.objects.all()
    translations = Translation.objects.all()
    return render(request, 'index.html', {"category": category, "translations": translations})


def index_category(request, category_name):
    category = Category.objects.all()
    translations = Translation.objects.all()
    return render(request, 'category.html', {"category": category, "translations": translations, "category_name": category_name})
