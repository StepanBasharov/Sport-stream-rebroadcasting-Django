# Generated by Django 4.1.4 on 2023-01-12 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0028_alter_category_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubs',
            name='end_sub',
            field=models.DateField(null=True, verbose_name='Конец действия подписки'),
        ),
    ]