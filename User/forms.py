#coding:utf-8
from django import forms

class Register_Forms(forms.Form):
    username = forms.CharField(max_length=32, label="用户名称",widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=16, label="用户密码",widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="用户邮箱",widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=18, label="用户手机",widget=forms.TextInput(attrs={'class':'form-control'}))
    # photo = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data.get("username","")
        if  username and len(username) < 6:
            raise forms.ValidationError("用户名至少要有6位")
        if username and not username.isalnum():
            raise forms.ValidationError("用户名中不可以有特殊符号")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password","")
        if password and len(password) < 6:
            raise forms.ValidationError("密码不能少于6位")
        return password


