#coding:utf-8
from django.shortcuts import render_to_response
from User.models import *

# Create your views here.

def Userlist(request):
    statue = "用户列表"
    AllUser = User.objects.all()
    return render_to_response("userlist.html",locals())