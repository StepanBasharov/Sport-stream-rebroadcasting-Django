from django.db import models
from django.contrib.auth.models import User
import datetime


class Category(models.Model):
    name = models.CharField("Название категории", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Translation(models.Model):
    is_pay_type = (('Платно', 'Платно'),
                   ('Бесплатно', 'Бесплатно'))
    name = models.CharField("Название трансляции", max_length=64)
    preview = models.ImageField("Превью", upload_to='images')
    first_team_flag = models.ImageField("Флаг первой команды", upload_to='images')
    second_team_flag = models.ImageField("Флаг второй команды", upload_to='images')
    first_team = models.CharField("Название первой команды", max_length=30, default="Команда 1")
    second_team = models.CharField("Название второй команды", max_length=30, default="Команда 2")
    date = models.DateField("Дата события")
    time = models.TimeField("Время события")
    is_pay = models.CharField("Доступ к трансляции", choices=is_pay_type, max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.CharField("Ссылка на поток", max_length=200)
    description = models.TextField("Описание", max_length=3000, default="Прямая трансляция")
    permission = models.ForeignKey('Subscription', on_delete=models.CASCADE, null=True)
    is_live = models.BooleanField("LIVE", default=False)
    online = models.IntegerField("Смотрят сейчас", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Трансляция"
        verbose_name_plural = "Трансляции"


class News(models.Model):
    name = models.CharField("Название", max_length=100)
    text = models.TextField("Текст", max_length=30000)
    photo_author = models.TextField("Автор фото", max_length=100, default="Неизвестен")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview = models.ImageField("Фото", upload_to='images')
    date = models.DateField("Дата", null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Subscription(models.Model):
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sub_name = models.CharField("Название подписки", max_length=100)
    sup_price_month = models.CharField("Цена за месяц", max_length=100, null=True)
    sub_price_year = models.CharField("Цена за год", max_length=100, null=True)
    sub_price_year_month = models.CharField("Цена за месяц при годовой подписке", max_length=100, null=True)
    sub_price_year_discount = models.CharField("Скидка при покупке годовой подписки", max_length=100, null=True)

    def __str__(self):
        return self.sub_name

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class NewsComment(models.Model):
    text = models.TextField("Текст комментария", max_length=500)
    author = models.CharField("Автор", max_length=100)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к новостям"


class TranslationComment(models.Model):
    text = models.TextField("Текст коментария", max_length=500)
    author = models.CharField("Автор", max_length=100)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к трансляциям"


class UserSubs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    end_sub = models.DateField("Конец действия подписки", null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class TranslationChatMessages(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"Чат трансляции №{self.room}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения чата"
