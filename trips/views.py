# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
import trips.forms as forms
import trips.models as models


def index(request):

    template = 'trips/index.html'
    context = {
        'h1': 'Trip and template records',
        'title': 'The title',
        'tripForm': forms.TripRecord(),
        'trips': models.Trip.objects.all(),
    }

    return render(request, template, context)


def triptemplate(request, identifier):

    trip = None
    directory = None

    trips = models.Trip.objects.filter(id__startswith=identifier)

    if trips.count() == 1:
        trip = trips[0]

    template = 'trips/triptemplate.html'

    if request.POST:

        if request.FILES:
            trip.save(files=request.FILES)

        trip = models.Trip.objects.get(id=trip.id)

    # Read and analyse any gpx files
    gpxfiles = []

    for gpxfile in trip.directory().model['gpx']:
        filepath = os.path.join(trip.filespace(), gpxfile)
        if os.path.isfile(filepath):
            f = open(filepath)
            gpxf = models.GPXFile(f, trip)
            gpxfiles.append(gpxf.analyse())

    if trip:
        h1 = trip.name
    else:
        h1 = 'No trip record found'

    context = {
        'h1': h1,
        'identifier': identifier,
        'trip': trip,
        'trips': trips,
        'uploadFile': forms.UploadFile(),
        'forms': True,
        #'gpxfiles': gpxfiles,
    }

    return render(request, template, context)


def viewdata(request, command, identifier):
    template = 'trips/data.html'
    route = None
    track = None
    waypoint = None

    if command == 'route':
        pass
    elif command == 'track':
        track = models.Track.objects.get(id=identifier)
    elif command == 'waypoint':
        waypoint = models.Waypoint.objects.get(id=identifier)
        pass
    
    context = {
        'h1': "View a data record",
        'command': command,
        'identifier': identifier,
        'route': route,
        'track': track,
        'waypoint': waypoint,
    }
    return render(request, template, context)


def viewfile(request, identifier, filename):

    template = 'trips/viewfile.html'
    h1 = 'View a file'
    warnings = []

    trip = models.Trip.objects.get(id__startswith=identifier)
    filepath = os.path.join(trip.filespace(), filename)

    if filename in trip.directory().model['gpx']:
        h1 = 'Examine a gpx file'
        filetype = 'gpx'

        f = open(filepath)
        gpxf = models.GPXFile(f, trip)

    if request.GET:
        if ('command' in request.GET.keys() and
                request.GET['command'] == 'inject'):
            warnings.extend(gpxf.inject())

    context = {
        'h1': h1,
        'identifier': identifier,
        'filename': filename,
        'filetype': filetype,
        'trip': trip,
        'gpxf': gpxf,
        'gpxfile': gpxf.analyse(),
        'warnings': warnings,
    }

    return render(request, template, context)


