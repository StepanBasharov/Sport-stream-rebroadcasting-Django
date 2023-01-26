from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import psutil
import speedtest


def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


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


class StreamsStats(View):
    pass

