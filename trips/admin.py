# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import Template, Trip, Track, TrackSegment, TrackPoint, Waypoint
from models import Route, RoutePoint

admin.site.register(Template)
admin.site.register(Trip)
admin.site.register(Track)
admin.site.register(TrackSegment)
admin.site.register(TrackPoint)
admin.site.register(Route)
admin.site.register(RoutePoint)
admin.site.register(Waypoint)
