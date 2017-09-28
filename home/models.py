# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models

class Member(models.Model):

    name_first = models.CharField(max_length=255)
    name_last = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)


class Group(models.Model):

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Member, related_name='groups')


