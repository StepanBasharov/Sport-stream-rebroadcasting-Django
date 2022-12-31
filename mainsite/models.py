from django.db import models


class Category(models.Model):
    name = models.CharField("Название категории", max_length=64)

    def __str__(self):
        return self.name


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
    is_live = models.BooleanField("LIVE", default=False)

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=30000)
    photo_author = models.TextField(max_length=100, default="Неизвестен")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview = models.ImageField(upload_to='images')
    date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    sub_name = models.CharField(max_length=100)
    sup_price = models.CharField(max_length=100)
