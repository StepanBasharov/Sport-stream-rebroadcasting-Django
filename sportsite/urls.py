from django.contrib import admin
from django.urls import path
from mainsite import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('translation/<pk>', views.TranslationPage.as_view(), name='translation'),
    path('news/<pk>', views.NewsPage.as_view(), name='news_card'),
    path('newslist', views.NewsList.as_view(), name='news_list'),
    path('translationslist', views.TranslationsList.as_view(), name='translations_list'),
    path('subscription', views.SubPage.as_view(), name='subs')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)