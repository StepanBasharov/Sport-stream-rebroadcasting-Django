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


def run_ffmpeg(pid, screen_name):
    os.system(f"screen -dmS {screen_name} {pid}")


def kill(screen_name):
    os.system(f"screen -S {screen_name} -X quit")


class ServerStats(View):
    def get(self, request, *args, **kwargs):
        if request.user.username == "admin":
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            net = psutil.net_io_counters()
            net_sent = humansize(net.bytes_sent)
            net_get = humansize(net.bytes_recv)
            disk = psutil.disk_usage('/')[3]
            disk_free = humansize(psutil.disk_usage('/').free)
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
            domian = request.build_absolute_uri('/').split("/")[2].split(":")[0]
            pid = f"ffmpeg -re -i {input_link} -c copy -f flv -y rtmp://185.189.255.205/{output_link}"
            proc = multiprocessing.Process(target=run_ffmpeg, args=(pid, stream_name))
            proc.start()
            stream = Stream(
                name=stream_name,
                input_stream=input_link,
                output_stream="https://video." + domian + output_link + ".m3u8",
                stream_pid=pid,
                tmux_session=stream_name
            )
            stream.save()
            return render(request, 'new_stream.html')
        else:
            return HttpResponse("Доступ запрещен")


class StreamManger(View):
    def get(self, request, *args, **kwargs):
        stream = Stream.objects.all()
        return render(request, 'streams_manager.html', {"streams": stream})

    def post(self, request, *args, **kwargs):
        status = request.POST.get("status")
        stream = request.POST.get("stream")
        screen_name = Stream.objects.get(stream_pid=stream).tmux_session
        if status == "kill":
            kill(screen_name)

        return HttpResponse(f"{status}{screen_name}")
