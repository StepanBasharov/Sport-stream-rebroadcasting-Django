# Generated by Django 4.1.4 on 2022-12-12 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0013_alter_translation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='first_team',
            field=models.CharField(default='Команда 1', max_length=30),
        ),
        migrations.AddField(
            model_name='translation',
            name='second_team',
            field=models.CharField(default='Команда 2', max_length=30),
        ),
    ]
