from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Translation)
admin.site.register(TranslationComment)
admin.site.register(News)
admin.site.register(NewsComment)
admin.site.register(Subscription)
admin.site.register(UserSubs)
admin.site.register(TranslationChatMessages)
