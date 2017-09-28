# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models

KIT_CATEGORY = (
    ('camping', 'camping'),
    ('climbing', 'climbing'),
    ('clothing', 'clothing'),
    ('cooking/kitchen', 'cooking/kitchen'),
    ('cycle', 'cycle'),
    ('first aid', 'first aid'),
    ('food', 'food'),
    ('navigation', 'navigation'),
    ('personal', 'personal'),
    ('unclassified', 'unclassified'),
    ('vehicle', 'vehicle'),
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

POINT_TYPE = (
    ('campsite', 'campsite'),

)

REPORT_STATUS = (
    ('working', 'working'),
    ('pending', 'pending'),
    ('publshed', 'published'),
    ('withdrawn', 'withdrawn'),
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
    template, or created blank. A trup record will have a range of
    dates associated with it. GPX files can be uploaded to trip
    records, and the wypoints and

    """

    identifier = models.CharField(max_length=255, unique=True)

    trip_type = models.CharField(
        max_length=64, choices=TRIP_TYPE, default='template')

    name = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    days_length = models.IntegerField(default=1)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
    
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


class Template(TripTemplate):
    """A Template is a general plan for an expedition.
    """


    
class Trip(TripTemplate):
    """A trip is a plan for and record of an actual expedition."""

    start_date_planned = models.DateField(blank=True, null=True)
    end_date_planned = models.DateField(blank=True, null=True)

    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)







    
class Equipment(models.Model):
    """List of available gear."""

    kit_category = models.CharField(
        max_length=64, choices=KIT_CATEGORY, default='Unclassified')

    identifier = models.CharField(max_length=255, blank=True, null=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)


class GPXfile(models.Model):
    """Track files uploaded by the interface."""


    
class PointOfInterest(models.Model):
    """Outgoing points."""

    trip = models.ManyToManyField(Trip)
    template = models.ManyToManyField(Template)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

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
        """Return the name of the Topo250 map this point falls on.
        """

        topo50 = None
        return topo50


class Route(models.Model):
    """Outgoing linear features.

    These may be shared amongst trips and trip templates."""

    trip = models.ManyToManyField(Trip)
    template = models.ManyToManyField(Template)

    comment = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    extensions = models.CharField(max_length=255, blank=True, null=True)
    gtype = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    link_type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    points = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

    geom = models.MultiLineStringField(srid=SRID['WGS84'])

    def computeGPX(self):
        """Return a GPX object (string) from this route."""



class RoutePoint(models.Model):
    """Points associated with a route."""

    route = models.ForeignKey(Route)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])



class Track(models.Model):
    """Incoming linear features.

    A track may only belong to one trip record. The field names are
    taken from the GDAL file translator.

    """

    trip = models.ForeignKey(Trip)

    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    geom = models.MultiLineStringField(srid=SRID['WGS84'])

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)



class TrackSegment(models.Model):
    track = models.ForeignKey(Track)
    extensions = models.TextField(blank=True, null=True)

    
class TrackPoint(models.Model):
    """Incoming points associated with a track."""

    segment = models.ForeignKey(TrackSegment)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    course = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    speed = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    geom = models.PointField(srid=SRID['WGS84'])

    
class TripKit(models.Model):
    """Lists of equipment items chosen for this trip."""

    trip = models.ForeignKey(Trip)

    kit = models.OneToOneField(
        Equipment, on_delete=models.CASCADE, primary_key=True,
    )
    notes = models.TextField(blank=True, null=True)



class TripReport(models.Model):
    """A trip report records written and photographic reports of a trip.
    """

    trip = models.ForeignKey(Trip)
    
    status = models.CharField(
        max_length=64, choices=REPORT_STATUS, default='Unclassified')

    date_pub = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True,null=True)
    report_text = models.TextField(blank=True, null=True)


class Waypoint(models.Model):
    """Incoming points.

    A waypoint may belong to only one trip record."""

    trips = models.ForeignKey(Trip)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

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

