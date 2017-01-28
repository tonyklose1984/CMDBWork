#coding:utf-8

import os
import sys
import re
import subprocess
import psutil
import urllib
import urllib2
import uuid
import socket,fcntl,struct

def getHostName():
    with os.popen('hostname') as f:
        return f.read()

def getIPaddr(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

def getMacaddr():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def getCore():
    with os.popen("uname -r") as f:
        return f.read()

def getData(path):
    all_dict = {}
    with open(path,'r') as f:
        content = f.readlines()
    for line in content:
        try:
            data_list1 = line.split(":")
            all_dict[data_list1[0].strip()] = data_list1[1].strip()
        except:
            pass
        try:
            data_list2 = line.split("=")
            all_dict[data_list2[0].strip()] = data_list2[1].strip()
        except:
            pass
    return all_dict
data = {}

data["Sys"] = getData("/etc/os-release")["NAME"]
data["Core"] = getCore().strip()
data["HostName"] = getHostName().strip()
data["IP"] = getIPaddr("eno16777736")
data["Mac"] = getMacaddr()
data["cpus"] = getData("/proc/cpuinfo")["model name"]
data["mem"] = str(psutil.virtual_memory().total/1024/1024)+" MB"
data["disk"] = str(psutil.disk_usage("/").total/1024/1024)+" MB"
          
if __name__ == "__main__":
    datas = urllib.urlencode(data)
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    url = "http://192.168.0.87:8080/server/getData/"
    req = urllib2.Request(url,data=datas,headers=header)
    ope = urllib2.urlopen(req)
    print(ope.read())
