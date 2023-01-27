from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import psutil
import multiprocessing
import os
from .models import Stream


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def run_ffmpeg(input_link, output_link, domian):
    os.system(
        f"ffmpeg -re -i {input_link} -c copy -f flv -y rtmp://{domian}/{output_link}")


class ServerStats(View):
    def get(self, request, *args, **kwargs):
        if request.user.username == "admin":
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            net = psutil.net_io_counters()
            net_sent = humansize(net.bytes_sent)
            net_get = humansize(net.bytes_recv)
            disk = psutil.disk_usage('E:/')[3]
            disk_free = humansize(psutil.disk_usage('E:/').free)
            conn = len(psutil.net_connections())

            return render(request, 'server_stats.html',
                          {'cpu': cpu, 'memory': memory, 'net_sent': net_sent, 'net_get': net_get, 'disk': disk,
                           'disk_free': disk_free, 'conn': conn})
        else:
            return HttpResponse("Доступ Запрещен")


class StreamsNew(View):
    def get(self, request, *args, **kwargs):
        if request.user.username == "admin":
            return render(request, 'new_stream.html')
        else:
            return HttpResponse("Доступ запрещен")

    def post(self, request, *args, ):
        if request.user.username == "admin":
            stream_name = request.POST.get("stream_name")
            input_link = request.POST.get("stream_input_link")
            output_link = request.POST.get("stream_output_link")
            domian = request.build_absolute_uri('/')[:-1]
            proc = multiprocessing.Process(target=run_ffmpeg, args=(input_link, output_link, domian, ))
            proc.start()
            pid = proc.pid
            stream = Stream(
                name=stream_name,
                input_stream=input_link,
                output_stream=output_link,
                stream_pid=pid
            )
            stream.save()
            return render(request, 'new_stream.html')
        else:
            return HttpResponse("Доступ запрещен")
