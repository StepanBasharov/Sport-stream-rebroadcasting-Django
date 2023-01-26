from django.db import models


class Stream(models.Model):
    name = models.CharField("Название", max_length=100)
    input_stream = models.CharField("Входной поток", max_length=500)
    output_stream = models.CharField("Выходной поток", max_length=500)
    bitrate_video = models.CharField("Битрейт видео", max_length=100)
    bitrate_audio = models.CharField("Битрейт аудио", max_length=100)
    size = models.CharField("Разрешение (1920x1080)", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"
