


from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^([\w]+)/([0-9]*)', views.viewdata),
    url(r'^([0-9a-f\-]*)/file/([\-\w\s\.]*)', views.viewfile),    
    url(r'^([0-9a-f\-]*)$', views.triptemplate),
    url(r'^([0-9a-f\-]*)/$', views.triptemplate),
]
