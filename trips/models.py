# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models

import gpxpy
import os
import uuid

import trips.settings as settings

SRID = {
    'NZTM': 2193,
    'WGS84': 4326,
}


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

    The identifier should be a universal unique identifier

        import uuid
        uuid.uuid4().hex

    Should yield something like this 32 character string:

        70d0209ecd564104936dc2c09cfaeabe
    """

    TRIP_TYPE = (
        ('air', 'air'),
        ('boat', 'boat'),
        ('cycle', 'cycle'),
        ('road', 'road'),
        ('tramping', 'tramping'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    trip_type = models.CharField(
        max_length=64, choices=TRIP_TYPE, default='tramping')

    name = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    days_length = models.IntegerField(default=1)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def __get_absolute_url__(self):
        return os.path.join(settings.BASE_URL, self.identifier())

    url = property(__get_absolute_url__)


    def save(self, files=None, *args, **kwargs):
        """Save any uploaded file to filespace."""

        if not os.path.isdir(self.find_filespace()):
            self.make_filespace()
            
        if files:
            for item in files:
                print "ITEM", item, type(item)
                f = files[item]
                print "F", f, type(f)
                filepath = os.path.join(self.find_filespace(), str(f))
                print "FILEPATH", filepath
                with open(filepath, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

        

        super(TripTemplate, self).save(*args, **kwargs)

        
    
    def identifier(self):
        """The first eight characters of the uuid, chopped by hyphen."""
        
        uri_steps =  str(self.id).split('-')
        return uri_steps[0]

    def find_filespace(self):
        """Return a string pathname to this object's filespace in static files.
        """

        dirname = self.name.replace(' ', '-').replace("'", "")
        dirname = dirname + '_' + self.identifier()

        filepath = os.path.join(
            settings.STATICFILES_DIR, settings.BASE_FILESPACE, dirname
        )

        return filepath

    def make_filespace(self):
        if not os.path.isdir(self.find_filespace()):
            os.mkdir(self.find_filespace())
            return True
        return False

        
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


class TemplateNote(models.Model):
    """Simple text notes attached to a template record."""

    trip = models.ForeignKey(Template)
    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)    
    
    
class Trip(TripTemplate):
    """A trip is a plan for and record of an actual expedition."""

    templates = models.ManyToManyField(Template)
    
    start_date_planned = models.DateField(blank=True, null=True)
    end_date_planned = models.DateField(blank=True, null=True)

    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)

    
class TripNote(models.Model):
    """Simple text notes attached to a trip record."""

    trips = models.ForeignKey(Trip, related_name='notes')
    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)    
    
    
class PointsOfInterest(models.Model):
    """Outgoing points.

    Points of interests are intended to be uploaded to a GPS device
    and used in the field. Waypoints are points generated in the field,
    which are downloaded into the database.

    """

    trips = models.ManyToManyField(Trip, related_name='pois')
    template = models.ManyToManyField(Template, related_name='pois')

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
    status = models.CharField(max_length=255, blank=True, null=True)
    
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

    trips = models.ManyToManyField(Trip)
    template = models.ManyToManyField(Template)

    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    points = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    geom = models.LineStringField(srid=SRID['WGS84'])

    def computeGPX(self):
        """Return a GPX object (string) from this route."""



class RoutePoint(models.Model):
    """Points associated with a route."""

    route = models.ForeignKey(Route)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    ordinal = models.IntegerField(default=0)
    status = models.CharField(max_length=255, blank=True, null=True)
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

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    geom = models.MultiLineStringField(srid=SRID['WGS84'], blank=True, null=True)


class TrackSegment(models.Model):
    track = models.ForeignKey(Track)
    extensions = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=255, blank=True, null=True)
    geom = models.LineStringField(srid=SRID['WGS84'], blank=True, null=True)

    
class TrackPoint(models.Model):
    """Incoming points associated with a track."""

    segment = models.ForeignKey(TrackSegment)

    age_of_dgps_data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    course = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dgps_id = models.TextField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    speed = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    ordinal = models.IntegerField(default=0)
    status = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PointField(srid=SRID['WGS84'])

    
class TripReport(models.Model):
    """A trip report records written and photographic reports of a trip.
    """

    STATUS = (
        ('working', 'working'),
        ('pending', 'pending'),
        ('publshed', 'published'),
        ('withdrawn', 'withdrawn'),
    )

    trip = models.ForeignKey(Trip)
    
    status = models.CharField(
        max_length=64, choices=STATUS, default='Unclassified')

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
    elevation = models.FloatField(blank=True, null=True)
    extensions = models.TextField(blank=True, null=True)
    geoid_height = models.TextField(blank=True, null=True)
    horizontal_dilution = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    link_text = models.TextField(blank=True, null=True)
    link_type = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    magnetic_variation = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    position_dilution = models.TextField(blank=True, null=True)
    satellites = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    gtype = models.TextField(blank=True, null=True)
    type_of_gpx_fix = models.TextField(blank=True, null=True)
    vertical_dilution = models.TextField(blank=True, null=True)

    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

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

class GPXFile():
    """Class to pocess a gpx file from upload or other place.

    Consumes an element from request.FILES, or an opened file.

    Will insert records into the database. 
    """

    gpx = None # Parsed gpxpy object
    trip = None # A Trip object.
    warnings = [] # List of strings.

    def __init__(self, gpxfile, trip):
        """Parse the file with gpxpy.

        A GPX file must be associated with an existing trip record.
        """

        self.gpxfile = gpxfile
        self.trip = trip
        self.gpx = gpxpy.parse(gpxfile)

        self.warnings.append("Processing gpxfile...")

        self.warnings.extend(self.process_waypoints(self.gpx))


    def process_waypoints(self, gpx):
        """Extract waypoint data from GPX file, insert records into db.
        """

        warnings = [str(len(gpx.waypoints)) + ' waypoints']
        
        for waypoint in gpx.waypoints:

            print "mag var", type(waypoint.magnetic_variation)

            existing = Waypoint.objects.filter(
                time=waypoint.time, latitude=waypoint.latitude,
                longitude=waypoint.longitude,
            )

            data = {
                'trip': self.trip_id,
                'age_of_dgps_data': waypoint.age_of_dgps_data,
                'comment': waypoint.comment,
                'description': waypoint.description,
                'dgps_id': waypoint.dgps_id,
                'elevation': waypoint.elevation,
                'extensions': waypoint.extensions,
                'geoid_height': waypoint.geoid_height,
                'horizontal_dilution': waypoint.horizontal_dilution,
                'latitude': waypoint.latitude,
                'link': waypoint.link,
                'link_text': waypoint.link_text,
                'link_type': waypoint.link_type,
                'longitude': waypoint.longitude,
                'magnetic_variation': waypoint.magnetic_variation,
                'name': waypoint.name,
                'position_dilution': waypoint.position_dilution,
                'satellites': waypoint.satellites,
                'source': waypoint.source,
                'symbol': waypoint.symbol,
                'time': waypoint.time,
                'gtype': waypoint.type,
                'type_of_gpx_fix': waypoint.type_of_gpx_fix,
                'vertical_dilution': waypoint.vertical_dilution,
            }
            
            p = Waypoint(**data)

            
            warnings.append(
                " ".join(
                    (waypoint.name,
                    str(waypoint.latitude),
                     str(waypoint.longitude),
                    )
                )
            )

        return warnings
