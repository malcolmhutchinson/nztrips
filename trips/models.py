# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, LineString, MultiLineString
from django.utils.timezone import make_aware

import gpxpy
import os
import uuid

import webnote

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

    def waypoints(self):
        return Waypoint.objects.filter(trip=self)

    def parse_filespace(self):
        """Return a webnote.Directory object of the filespace."""

        filespace = self.filespace()
        if not os.path.isdir(filespace):
            self.make_filespace()
        directory = webnote.Directory(filespace)

        return directory

    def save(self, files=None, *args, **kwargs):
        """Save any uploaded file to filespace."""

        if not os.path.isdir(self.filespace()):
            self.make_filespace()

        if files:
            for item in files:

                f = files[item]
                filepath = os.path.join(
                    self.filespace(), str(f))

                with open(filepath, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

        super(TripTemplate, self).save(*args, **kwargs)


    def identifier(self):
        """The first eight characters of the uuid, chopped by hyphen."""

        uri_steps =  str(self.id).split('-')
        return uri_steps[0]

    def filespace(self):
        """Return a string pathname to this object's filespace in static files.
        """

        dirname = self.name.replace(' ', '-').replace("'", "")
        dirname = dirname + '_' + self.identifier()

        filepath = os.path.join(
            settings.STATICFILES_DIR, settings.BASE_FILESPACE, dirname
        )

        return filepath

    def make_filespace(self):
        if not os.path.isdir(self.filespace()):
            os.mkdir(self.filespace())
            return True
        return False


class Template(TripTemplate):
    """A Template is a general plan for an expedition.
    """


class TemplateNote(models.Model):
    """Simple text notes attached to a template record."""

    template = models.ForeignKey(Template)
    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)


class Trip(TripTemplate):
    """A trip is a plan for and record of an actual expedition."""

    templates = models.ManyToManyField(Template)

    start_date_planned = models.DateField(blank=True, null=True)
    end_date_planned = models.DateField(blank=True, null=True)

    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)


class TripNote(models.Model):
    """Simple text notes attached to a trip record."""

    trip = models.ForeignKey(Trip, related_name='notes')
    owner = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    geom = models.PointField(srid=SRID['WGS84'])




class Route(models.Model):
    """Outgoing linear features.

    These may be shared amongst trips and trip templates."""

    trips = models.ManyToManyField(Trip)
    templates = models.ManyToManyField(Template)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

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

    trip = models.ForeignKey(Trip)

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
    provenance = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    geom = models.PointField(srid=SRID['WGS84'])

    def __unicode__(self):
        return self.name

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

        Instantiate with a file, from request.FILES, or the result of
        a file open operation.

        Data from a GPX file must be associated with an existing trip
        record.
        """

        self.gpxfile = gpxfile
        self.trip = trip
        self.gpx = gpxpy.parse(gpxfile)

    def __get_absolute_url__(self):

        (path, fname) = os.path.split(self.gpxfile.name)
        return os.path.join(self.trip.url, 'file', fname)

    url = property(__get_absolute_url__)

    def analyse(self):
        """Return a dictionary containing lists of points, lines etc.

        Indicate whether a record exists in the db matching this one.
        """

        (path, name) = os.path.split(self.gpxfile.name)

        result = {
            "name": name,
            "url": self.url,
            "routes": self.analyse_routes(),
            "tracks": self.analyse_tracks(),
            "waypoints": self.analyse_waypoints(),
        }

        return result

    def analyse_routes(self):
        """List basic data about each route."""

        result = []
        return result

    def analyse_tracks(self):
        """List basic data about each track."""

        result = []

        for track in self.gpx.tracks:
            track = {
                "name": track.name
            }
            result.append(track)

        return result

    def analyse_waypoints(self):
        """List basic data about each waypoint."""

        result = []

        for waypoint in self.gpx.waypoints:
            point = {
                "name": waypoint.name,
                "comment": waypoint.comment,
                "latitude": waypoint.latitude,
                "longitude": waypoint.longitude,
            }

            result.append(point)

        return result


    def inject(self):
        """Sequencer for the injection operation. Calls waypoints etc."""

        warnings = []
        warnings.extend(self.inject_tracks(self.gpx, self.trip))
        warnings.extend(self.inject_waypoints(self.gpx, self.trip))

        return warnings

    def inject_routes(self, gpx, trip):

        warnings = []

        return warnings

    def inject_tracks(self, gpx, trip):

        warnings = []
     
        (path, provenance) = os.path.split(self.gpxfile.name)

        for track in gpx.tracks:

            existing = Track.objects.filter(
                name=track.name, number=track.number
            )
            if existing.count() > 0:
                
                data = {
                    'trip': trip,
                    'comment': track.comment,
                    'description': track.description,
                    'extensions': track.extensions,
                    'gtype': track.type,
                    'link': track.link,
                    'link_text': track.link_text,
                    'link_type': track.link_type,
                    'name': track.name,
                    'number': track.number,
                    'source': track.source,

                    'owner': None,
                    'group': None,
                    'status': None,
                    'provenance': provenance,
                }

                for item in sorted(data.keys()):
                    print item, data[item]

                #track = Track(**data)

                for segment in track.segments:
                    print segment



        
        return warnings

    def inject_waypoints(self, gpx, trip):
        """Extract waypoint data from gpxpy object, insert records into db.
        """

        warnings = ['Injecting ' + str(len(gpx.waypoints)) + ' waypoints.']

        for waypoint in gpx.waypoints:

            existing = Waypoint.objects.filter(
                time=waypoint.time, latitude=waypoint.latitude,
                longitude=waypoint.longitude,
            )
            if existing.count() > 0:
                warnings.append(waypoint.name + " found in db.")

            else:
                
                (path, provenance) = os.path.split(self.gpxfile.name)

                data = {
                    'trip': trip,
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
                    'time': make_aware(waypoint.time),
                    'gtype': waypoint.type,
                    'type_of_gpx_fix': waypoint.type_of_gpx_fix,
                    'vertical_dilution': waypoint.vertical_dilution,

                    'owner': None,
                    'group': None,
                    'status': None,
                    'provenance': provenance,
                    'geom': Point(
                        waypoint.latitude, waypoint.longitude, srid=4326),
                    
                }

                p = Waypoint(**data)
                p.save()
                
                warnings.append(
                    " ".join(
                        (waypoint.name,
                        str(waypoint.latitude),
                         str(waypoint.longitude),
                        )
                    )
                )

        return warnings
