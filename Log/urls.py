from django.conf.urls import include,url
from views import *

urlpatterns = [
    url(r'get_log',get_log),
    url(r'set_log',Logs),
]