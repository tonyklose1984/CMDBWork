#coding:utf-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from Service.models import *
from django.http import JsonResponse
import datetime
from Api.views import Remote
from Api.views import *
from CMDBWork.views import *

@login_valid
def serverInfo(request):
    statue = "服务器列表"
    serverdata = Service.objects.all()
    return render_to_response("serverinfo.html",locals())

def getDate(request):
    response_dict = {"status":"success","time":datetime.datetime.now()}
    if request.method == "POST" and request.POST:
        Sys = request.POST.get("Sys")
        Core = request.POST.get("Core")
        HostName = request.POST.get("HostName")
        IP = request.POST.get("IP")
        Mac = request.POST.get("Mac")
        cpus = request.POST.get("cpus")
        mem = request.POST.get("mem")
        disk = request.POST.get("disk")
        ser = Service(
            host = HostName,
            ip =IP,
            mac = Mac,
            cpu = cpus,
            mem = mem,
            disk = disk,
            system = Sys,
            model= Core,
        )
        ser.save()
    else:
        response_dict["status"]="error"

    return JsonResponse(response_dict)

def content(request,ids):
    service_data = Service.objects.get(id = int(ids))
    user_list = ServerUser.objects.filter(serviceid=ids)
    hostname = service_data.host.strip()
    statue = "%s 详情页"%hostname.encode("utf-8")
    host_data = {
        "host_name":service_data.host,
        "ip":service_data.ip,
        "mac":service_data.mac,
        "cpu":service_data.cpu,
        "mem":service_data.mem,
        "disk":service_data.disk,
        "system":service_data.system,
        "model":service_data.model,
        "id":service_data.id,
    }
    return render_to_response("server_content.html",locals())

def getCpu(reqeust):
    if reqeust.method == "GET" and reqeust.GET:
        print(reqeust.GET)
        serverId = reqeust.GET.get("serverId")
        cpuData = CpuData.objects.filter(serviceid=int(serverId)).order_by("-time")[0:20]
        cpu_list = []
        for num,cpu in enumerate(cpuData):
            cpu_dict = {}
            cpu_dict["data"] = cpu.cpuload
            cpu_dict["year"] = cpu.time.strftime("%Y-%m-%dT%H:%M:%S")
            cpu_list.append(cpu_dict)
        return JsonResponse({"data":cpu_list})
    else:
        return JsonResponse({"err":"method must be get"})







# Create your views here.

@login_valid
def Shell(request):
    statue = "Remote Shell"
    if request.method == "POST" and request.POST:
        print(request.POST)
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        command = request.POST.get('command')
        remote = Remote(ip,username,passwd,int(port))
        result = remote.ssh(command)
        if isinstance(result,bool):
            return HttpResponse('<h2>The remote connection failed...,please try again.')
        else:
            result = [line.replace(' ','&nbsp') for line in result]
            print(result)
        return render(request,"RemoteShell.html",locals())

    return render(request, "RemoteShell.html", locals())