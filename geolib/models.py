# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models

# Create your models here.
class Topo250(models.Model):
    """Contains the Topo50 mapping grid without map sheet overlays.
    """

    identifier = models.CharField(max_length=4, primary_key=True)
    sheet_name = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=2193)

    nzms_xmax = models.IntegerField()
    nzms_xmin = models.IntegerField()
    nzms_ymax = models.IntegerField()
    nzms_ymin = models.IntegerField()


class Topo50(models.Model):
    """Contains the Topo50 mapping grid without map sheet overlays.
    """

    identifier = models.CharField(max_length=4, primary_key=True)
    sheet_name = models.TextField(blank=True, null=True)
    geom = models.PolygonField(srid=2193)

    nzms_xmax = models.IntegerField()
    nzms_xmin = models.IntegerField()
    nzms_ymax = models.IntegerField()
    nzms_ymin = models.IntegerField()

