#coding:utf-8
from django.shortcuts import render_to_response
from django.http import JsonResponse
import datetime
from forms import *
from models import *


def setLog(user,time,operation,level,type):
    log = Log()
    log.user = user
    log.time = time
    log.operation = operation
    log.level = level
    log.type = type
    log.save()
    return {"statue":"sucess"}

def set_log(request):
    if request.method == "POST" and request.POST:
        result = setLog(
        user = request.POST.get("user"),
        time = datetime.datetime.now(),
        operation = request.POST.get("operation"),
        level = request.GET.POST("level"),
        type = request.GET.POST("type"),
        )
    else:
        result = {"statue":"post error"}
    return JsonResponse(result)

def get_log(request):
    '''
    获取单条日志信息
    '''
    statue = "日志查询"
    result = {"statue":"","data":""}
    if request.method == "GET" and request.GET:
        log = Log.objects.get(id = int(request.GET.get("id")))
    else:
        log = {}
    return render_to_response("logread.html",locals())

def all_log(request):
    '''
    获取所有日志信息
    '''
    allLog = Log.objects.all()
    result = {}
    log_list = []
    for log in allLog:
        log_dict = {
            "id":log.id,
            "user":log.user,
            "time":log.time,
            "operation":log.operation,
            "level":log.level,
            "type":log.type
        }
        log_list.append(log_dict)
    result["data"] = log_list
    return JsonResponse(result)

def Logs(request):
    statue = "日志记录"
    if request.method == "POST" and request.POST:
        logs_form = Log_Forms(request.POST)
        if logs_form.is_valid():
            clear_data = logs_form.cleaned_data
            logs = Log(
                user = request.POST.get('username'),
                time = datetime.datetime.now(),
                operation = request.POST.get('operation'),
                level = request.POST.get('level'),
                type = request.POST.get('type'),
            )
            logs.save()
            return JsonResponse({"result":"success"})
    else:
        logs_form = Log_Forms()
    return render_to_response("log.html",locals())


# Create your views here.
