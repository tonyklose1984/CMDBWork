from django.shortcuts import render_to_response
from Service.models import *
from Service.views import *
from User.models import *
from django.http import JsonResponse
import paramiko
import re
import time
import datetime

def savedata(request):
    result = {}
    if request.method == "POST" and request.POST:
        req_data = request.POST
        service = Service()
        service.host = req_data.get("host")
        service.ip = req_data.get("ip")
        service.mac = req_data.get("mac")
        service.cpu = req_data.get('cpu')
        service.mem = req_data.get('mem')
        service.disk = req_data.get('disk')
        service.system = req_data.get('system')
        service.model = req_data.get('model')
        service.save()
        result["statue"] = "sucess"
    else:
        result["statue"] = "error"
    return JsonResponse(result)

class Remote(object):
    def __init__(self,host,username,passwd,port=22):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd

    def ssh(self,command):
        self.command = command
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.passwd)
        except Exception as e:
            return False
        else:
            ssh = paramiko.SSHClient()
            ssh._transport = transport
            stdin, stdout, stderr = ssh.exec_command(self.command)
            result = stdout.readlines()
            transport.close()
        return result

def setcpu(request):
    command = request.GET.get("command")
    ipaddr = request.GET.get("ipaddr").strip()
    userId = request.GET.get("userId")
    port = request.GET.get("port")
    serverId = request.GET.get("serverId")
    user = ServerUser.objects.get(id = int(userId))
    c = Remote(host=ipaddr,port=int(port),username=user.serverUserName,passwd=user.serverUserPasswd)
    result = [line.strip() for line in c.ssh(command)]
    print(len(result))
    for num,line in enumerate(result):
        if num >=2:
            cpuIDLE = re.split(r"\s+",line)[-3]
            # print cpuIDLE
            cpu_used = 100 - int(cpuIDLE)
            # print(cpu_used)
            cpu = CpuData()
            cpu.serviceid = int(serverId)
            cpu.cpuload = int(cpu_used)
            cpu.time = datetime.datetime.now()
            cpu.save()
        else:
            pass
    return JsonResponse({"statue":"success"})

def doCommand(request):
    command = request.GET.get("command")
    ipaddr = request.GET.get("ipaddr").strip()
    userId = request.GET.get("userId")
    port = int(request.GET.get("port",22))
    serverId = request.GET.get("serverId")
    user = ServerUser.objects.get(id=int(userId))
    c = Remote(ipaddr, user.serverUserName, user.serverUserPasswd,int(port))
    result = [line.strip() for line in c.ssh(command)]
    return JsonResponse({"result":result})

def test(request):
    result = {"state":""}
    if request.method == "GET" and request.GET:
        result["state"] = "GET"
    else:
        result["state"] = "POST"
    return JsonResponse(result)

# Create your views here.
