#coding:utf-8
from django import forms
import datetime

class Log_Forms(forms.Form):
    username = forms.CharField(max_length=32, label="用户名称",widget=forms.TextInput(attrs={'class':'form-control'}))
    time = datetime.datetime.now()
    operation = forms.CharField(label="用户操作",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    level = forms.CharField(max_length=4, label="日志等级",widget=forms.TextInput(attrs={'class':'form-control'}))
    type = forms.CharField(max_length=128, label="日志类型", widget=forms.TextInput(attrs={'class': 'form-control'}))
