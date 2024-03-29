# Generated by Django 4.1.4 on 2022-12-12 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_remove_translation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='first_team_flag',
            field=models.ImageField(upload_to='mainsite/static/image'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='is_pay',
            field=models.CharField(choices=[('Платно', 'Платно'), ('Бесплатно', 'Бесплатно')], max_length=50),
        ),
        migrations.AlterField(
            model_name='translation',
            name='preview',
            field=models.ImageField(upload_to='mainsite/static/image'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='second_team_flag',
            field=models.ImageField(upload_to='mainsite/static/image'),
        ),
    ]
