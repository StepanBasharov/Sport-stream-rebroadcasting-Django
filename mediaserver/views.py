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


def run_ffmpeg(pid, tmux_session):
    os.system(f"tmux new-session -t {tmux_session}")
    os.system(f"{pid}")
    os.system("tmux detach")


def restart_ffmpeg(pid, tmux_session):
    os.system(f"tmux attach -t {tmux_session}")
    os.system(f"{pid}")
    os.system("tmux detach")


def kill(pid, tmux_session):
    os.system(f'tmux attach -t {tmux_session}')
    os.system(f'q')
    os.system(f'tmux kill-session -t {tmux_session}')
    Stream.objects.filter(stream_pid=pid).delete()


def stop(pid, tmux_session):
    os.system(f'tmux attach -t {tmux_session}')
    os.system(f"q")
    os.system(f"tmux detach")


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
            domian = request.build_absolute_uri('/').split("/")[2].split(":")[0]
            pid = f"ffmpeg -re -i {input_link} -c copy -f flv -y rtmp://{domian}{output_link}"
            proc = multiprocessing.Process(target=run_ffmpeg, args=(pid, stream_name))
            proc.start()
            stream = Stream(
                name=stream_name,
                input_stream=input_link,
                output_stream=domian + ":8080" + output_link + ".m3u8",
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
        tmux_session = Stream.objects.get(stream_pid=stream).tmux_session
        if status == "kill":
            kill(stream, tmux_session)
        elif status == "start":
            run_ffmpeg(stream, tmux_session)
        elif status == "stop":
            stop(stream, tmux_session)

        return HttpResponse(f"{status}{stream}")
