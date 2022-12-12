from django.shortcuts import render
from .models import Category, Translation


def index(request):
    category = Category.objects.all()
    translations = Translation.objects.all()
    return render(request, 'index.html', {"category": category, "translations": translations})
