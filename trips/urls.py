


from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^([0-9a-f\-]*)', views.triptemplate),
]
