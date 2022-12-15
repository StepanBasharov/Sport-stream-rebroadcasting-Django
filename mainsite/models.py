from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, default="slug")

    def __str__(self):
        return self.name


class Translation(models.Model):
    is_pay_type = (('Платно', 'Платно'),
                   ('Бесплатно', 'Бесплатно'))
    name = models.CharField(max_length=64)
    preview = models.ImageField(upload_to='images')
    first_team_flag = models.ImageField(upload_to='images')
    second_team_flag = models.ImageField(upload_to='images')
    first_team = models.CharField(max_length=30, default="Команда 1")
    second_team = models.CharField(max_length=30, default="Команда 2")
    date = models.DateField()
    time = models.TimeField()
    is_pay = models.CharField(choices=is_pay_type, max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name
