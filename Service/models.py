#coding:utf-8
from django.db import models

class Service(models.Model):
    host = models.CharField(max_length=32,verbose_name="主机名称")
    ip = models.CharField(max_length=32,verbose_name="主机IP")
    mac = models.CharField(max_length=32,verbose_name="主机mac")
    cpu = models.CharField(max_length=32,verbose_name="cpu")
    mem = models.CharField(max_length=32,verbose_name="mem")
    disk = models.CharField(max_length=32,verbose_name="disk")
    system = models.CharField(max_length=32,verbose_name="system")
    model = models.CharField(max_length=32,verbose_name="主机型号")

class CpuData(models.Model):
    serviceid = models.IntegerField(verbose_name="主机id")
    cpuload = models.IntegerField(verbose_name="CPU使用率")
    time = models.DateTimeField(verbose_name="监控时间")

class ServerUser(models.Model):
    serviceid = models.IntegerField(verbose_name="主机id")
    serverUserName = models.CharField(max_length=32,verbose_name="服务器用户名")
    serverUserPasswd = models.CharField(max_length=32,verbose_name="服务器密码")



# Create your models here.
