# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models

KIT_CATEGORY = (
    ('Camping', 'Camping'),
    ('Climbing', 'Climbing'),
    ('Clothing', 'Clothing'),
    ('Cooking/kitchen', 'Cooking/kitchen'),
    ('Cycle', 'Cycle'),
    ('First aid', 'First aid'),
    ('Food', 'Food'),
    ('Navigation', 'Navigation'),
    ('Personal', 'Personal'),
    ('Unclassified', 'Unclassified'),
    ('Vehicle', 'Vehicle'),
)

QGIS_FIELDS = (
    'name',
    'symbol',
    'number',
    'comment',
    'description',
    'source',
    'url',
    'urlname',
)

REPORT_STATUS = (
    ('Working', 'Working'),
    ('Pending', 'Pending'),
    ('Publshed', 'Published'),
    ('Withdrawn', 'Withdrawn'),
)

SRID = {
    'NZTM': 2193,
    'WGS84': 4326,
}


TRIPRECORD_CLASS = (
    ('template', 'template'),
    ('trip', 'trip'),
)

TRIP_TYPE = (
    ('air', 'air'),
    ('boat', 'boat'),
    ('cycle', 'cycle'),
    ('road', 'road'),
    ('tramping', 'tramping'),
)

# Create your models here.
class TripTemplate(models.Model):
    """Trip and template objects.

    A template records a plan for an excursion. It may have many
    points of interest and routes associated with it, and other
    documents and file.

    A trip plans for and records an event. It may be cloned from a
    template, or created blank. A trip record will have a range of
    dates associated with it. GPX files can be uploaded to trip
    records, and any waypoints, tracks our rutes in that file injected
    into the datbase.

    """

    identifier = models.CharField(max_length=255, unique=True)
    record_class = models.CharField(
        max_length=64, choices=TRIPRECORD_CLASS, default='template')

    trip_type = models.CharField(
        max_length=64, choices=TRIP_TYPE, default='template')

    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)

    start_date_planned = models.DateField(blank=True, null=True)
    end_date_planned = models.DateField(blank=True, null=True)

    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)

    def computeGPX(self):
        """Return a GPX object from all routes and POIs in this trip."""

        gpx = ''
        return gpx

    def topo250maps(self):
        """Return a list of the Topo250 maps touched by this trip."""

        maps = []
        return maps

    def topo50maps(self):
        """Return a list of the Topo50 maps touched by this trip."""

        maps = []
        return maps


class Equipment(models.Model):
    """List of available gear."""

    trip = models.ManyToManyField(TripTemplate)

    kit_category = models.CharField(
        max_length=64, choices=KIT_CATEGORY, default='Unclassified')

    identifier = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

class PointsOfInterest(models.Model):
    """Outgoing points.

    Points of interests are intended to be uploaded to a GPS device
    and used in the field. Waypoints are points generated in the field,
    which are downloaded into the database.

    """

    templates = models.ManyToManyField(TripTemplate)
    trips = models.ManyToManyField(TripTemplate)

    name = models.CharField(max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    urlname = models.CharField(max_length=255, blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])

    def nztm(self):
        """Return a geometry representing this point in NZTM 2000.
        """

    def topo250map(self):
        """Return the name of the Topo250 map this point falls on.
        """

        topo250 = None
        return topo250

    def topo50map(self):
        """Return the name of the Topo50 map this point falls on.
        """

        topo50 = None
        return topo50


class Route(models.Model):
    """Outgoing linear features.

    These may be shared amongst trips and trip templates."""

    templates = models.ManyToManyField(TripTemplate)
    trips = models.ManyToManyField(TripTemplate)

    geom = models.MultiLineStringField(srid=SRID['WGS84'])

    def computeGPX(self):
        """Return a GPX object (string) from this route."""

    def computePoints(self):
        """Return a list of points extracted from the linestring geom.

        The list will be suitable for injecting into the database,
        replacing any which may already be associated with this route.

        """

class RoutePoint(models.Model):
    """Points associated with a route."""

    route = models.ForeignKey(Route)

    name = models.CharField(max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    urlname = models.CharField(max_length=255, blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])


class Track(models.Model):
    """Incoming linear features.

    A track may only belong to one trip record.
    """

    trips = models.ForeignKey(TripTemplate)

    name = models.CharField(max_length=255, blank=True, null=True)
    cmt = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    link1_href = models.CharField(max_length=255, blank=True, null=True)
    link1_text = models.CharField(max_length=255, blank=True, null=True)
    link1_type = models.CharField(max_length=255, blank=True, null=True)
    link2_href = models.CharField(max_length=255, blank=True, null=True)
    link2_text = models.CharField(max_length=255, blank=True, null=True)
    link2_type = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    gpxtype = models.CharField(max_length=255, blank=True, null=True)
    gpxx_TrackExtension = models.CharField(max_length=255, blank=True, null=True)

    geom = models.MultiLineStringField(srid=SRID['WGS84'])

    owner = models.CharField(max_length=255, blank=True, null=True)
    acquired = models.DateTimeField(blank=True, null=True)


class TrackPoint(models.Model):
    """Incoming points associated with a track."""

    track = models.ForeignKey(Track)

    track_fid = models.IntegerField(blank=True, null=True, default=0)
    track_seg_id = models.IntegerField(blank=True, null=True, default=0)
    track_seg_point = models.IntegerField(blank=True, null=True, default=0)
    ele = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    magvar = models.CharField(max_length=255, blank=True, null=True)
    geoidheight = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cmt = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    link1_href = models.CharField(max_length=255, blank=True, null=True)
    link1_text = models.CharField(max_length=255, blank=True, null=True)
    link1_type = models.CharField(max_length=255, blank=True, null=True)
    link2_href = models.CharField(max_length=255, blank=True, null=True)
    link2_text = models.CharField(max_length=255, blank=True, null=True)
    link2_type = models.CharField(max_length=255, blank=True, null=True)
    sym = models.CharField(max_length=255, blank=True, null=True)
    gpsxtype = models.CharField(max_length=255, blank=True, null=True)
    fix = models.CharField(max_length=255, blank=True, null=True)
    sat = models.CharField(max_length=255, blank=True, null=True)
    hdop = models.CharField(max_length=255, blank=True, null=True)
    vdop = models.CharField(max_length=255, blank=True, null=True)
    pdop = models.CharField(max_length=255, blank=True, null=True)
    ageofgpdsata = models.CharField(max_length=255, blank=True, null=True)
    dgpsid = models.CharField(max_length=255, blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])


class TripKit(models.Model):
    """Lists of equipment items chosen for this trip."""

    trip = models.ForeignKey(TripTemplate)
    kit = models.OneToOneField(
        Equipment, on_delete=models.CASCADE, primary_key=True,
    )
    notes = models.TextField(blank=True, null=True)



class TripReport(models.Model):
    """A trip report records written and photographic reports of a trip.
    """

    trip = models.ForeignKey(TripTemplate)
    status = models.CharField(
        max_length=64, choices=REPORT_STATUS, default='Unclassified')

    date_pub = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True,null=True)
    report_text = models.TextField(blank=True, null=True)


class Waypoint(models.Model):
    """Incoming points.

    A waypoint may belong to only one trip record."""

    trips = models.ForeignKey(TripTemplate)

    ele = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    magvar = models.CharField(max_length=255, blank=True, null=True)
    geoidheight = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cmt = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    link1_href = models.CharField(max_length=255, blank=True, null=True)
    link1_text = models.CharField(max_length=255, blank=True, null=True)
    link1_type = models.CharField(max_length=255, blank=True, null=True)
    link2_href = models.CharField(max_length=255, blank=True, null=True)
    link2_text = models.CharField(max_length=255, blank=True, null=True)
    link2_type = models.CharField(max_length=255, blank=True, null=True)
    sym = models.CharField(max_length=255, blank=True, null=True)
    gpsxtype = models.CharField(max_length=255, blank=True, null=True)
    fix = models.CharField(max_length=255, blank=True, null=True)
    sat = models.CharField(max_length=255, blank=True, null=True)
    hdop = models.CharField(max_length=255, blank=True, null=True)
    vdop = models.CharField(max_length=255, blank=True, null=True)
    pdop = models.CharField(max_length=255, blank=True, null=True)
    ageofgpdsata = models.CharField(max_length=255, blank=True, null=True)
    dgpsid = models.CharField(max_length=255, blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])

    def nztm(self):
        """Return a geometry representing thsi point in NZTM 2000.
        """

    def topo250map(self):
        """Return the name of the Topo250 map this point falls on.
        """

        topo250 = None
        return topo250

    def topo50map(self):
        """Return the name of the Topo250 map this point falls on.
        """

        topo50 = None
        return topo50
