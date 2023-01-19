from django.contrib import admin
from django.contrib.auth import logout
from django.template.defaulttags import url
from django.urls import path, include
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
    path('subscription', views.SubPage.as_view(), name='subs'),
    path('login', views.Login.as_view(), name='login'),
    path(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('registration', views.Register.as_view(), name='registration'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('news/<pk>/like/', views.AddLike.as_view(), name='like'),
    path('news/<pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
    path('news/<pk>/comment', views.NewNewsComment.as_view(), name='comment'),
    path('translation/<pk>/comment', views.NewTranslationComment.as_view(), name='chat'),
    path('profile', views.UserProfile.as_view(), name='profile'),
    path('rename', views.rename, name='rename'),
    path('changemail', views.new_mail, name='changemail'),
    path('resetpassword', views.set_new_password, name='resetpassword'),
    path('search', views.Search.as_view(), name='search'),
    path('about', views.AboutUs.as_view(), name='about'),
    path('contacts', views.Contacts.as_view(), name='contacts')
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)