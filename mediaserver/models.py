from django.db import models


class Stream(models.Model):
    name = models.CharField("Название", max_length=100)
    input_stream = models.CharField("Входной поток", max_length=500)
    output_stream = models.CharField("Выходной поток", max_length=500)
    stream_pid = models.CharField("PID", max_length=100, default="0000")
    tmux_session = models.CharField("TMUX", max_length=100, default="sess")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"

