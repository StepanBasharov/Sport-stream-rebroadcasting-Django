# Generated by Django 4.1.4 on 2023-01-28 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaserver', '0002_remove_stream_bitrate_audio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='tmux_session',
            field=models.CharField(default='sess', max_length=100, verbose_name='TMUX'),
        ),
    ]
