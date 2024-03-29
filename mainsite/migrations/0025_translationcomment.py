# Generated by Django 4.1.4 on 2023-01-09 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0024_alter_news_date_alter_news_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Текс Коментария')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.translation')),
            ],
        ),
    ]
