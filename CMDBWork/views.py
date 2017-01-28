#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from User.forms import *
import hashlib
from User.models import User

def hashpassword(password):
    '''
    系统密码采用MD5加密
    '''
    h = hashlib.md5()
    h.update(password)
    return h.hexdigest()

def user_exist(username): #检查是否有重复的用户名
    try:
        User.objects.get(username=username)
        return True
    except:
        return False

def user_valid(username,passwd): #验证登陆账户
    try:
        user = User.objects.get(username=username)
        if user.password == hashpassword(passwd):
            return True
        else:
            return False
    except:
        return False

def login_valid(func):
    def inner(request,*args,**kwargs):
        try:
            username = request.session["username"]
            return func(request)
        except KeyError as e:
            if repr(e) == "KeyError('username',)":
                err = "当前用户未登录请登录"
            else:
                err = str(e)
            url = "/404/"+err
            return HttpResponseRedirect(url)
    return inner

@login_valid
def index(request):
    statue = "运维首页"
    return render_to_response("index.html",locals())

def forms(request):
    return render_to_response("forms.html",locals())

def forbiden(request,error):
    return render_to_response("404.html",locals())

def base(request):
    return render_to_response("base.html",locals())

def login(request):
    result = {}
    if request.method == "POST" and request.POST:
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username and password and user_valid(username,password):
            response = HttpResponseRedirect("/index")
            response.set_cookie("username",username)
            request.session["username"] = username
            return response
        else:
            result["error"] = "用户名或者密码错误"
            return render_to_response("login.html",locals())
    else:
        return render_to_response("login.html",locals())

def logout(request):
    del request.COOKIES["username"]
    del request.session["username"]
    return render_to_response("logout.html")

def register(request):
    statue = "用户注册"
    if request.method == "POST" and request.POST:
        registerForm = Register_Forms(request.POST)
        if registerForm.is_valid():
            clear_data = registerForm.cleaned_data
            u = User(
                username=clear_data.get('username'),
                password=hashpassword(clear_data.get("password")),
                email=clear_data.get("email"),
                phone=clear_data.get("phone"),
                    # photo=clear_data.get("photo"),
            )
            if user_exist(u.username):
                usererror = "您输入的用户名重复了，请重新输入"
                return render_to_response("register.html",locals())
            else:
                u.save()
                return HttpResponseRedirect('/login')
            # del request.COOKIES["username"]
            # del request.session["username"]

    else:
        registerForm =Register_Forms()
    return render_to_response("register.html",locals())



