# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
import trips.forms as forms
import trips.models as models

# Create your views here.
def index(request):

    template = 'trips/index.html'
    context = {
        'h1': 'Trip and template records',
        'title': 'The title',
        'tripForm': forms.TripRecord(),
        'trips': models.Trip.objects.all(),
    }

    return render(request, template, context)


def viewfile(request, identifier, filename):

    template = 'trips/viewfile.html'
    h1 = 'View a file'

    trip = models.Trip.objects.get(id__startswith=identifier)
    filepath = os.path.join(trip.filespace(), filename)
    

    if filename in trip.parse_filespace().model['gpx']:
        h1 = 'Examine a gpx file'
        filetype = 'gpx'

        f = open(filepath)
        gpxf = models.GPXFile(f, trip)

    
    # Inject one gpx file.
    #filepath = os.path.join(trip.filespace(), '2017-09-30 02.17.41 Day.gpx')
    #if os.path.isfile(filepath):
    #    f = open(filepath)
    #    injection = models.GPXFile(f, trip)
    #    injection.inject()
    

    
    context = {
        'h1': h1,
        'identifier': identifier,
        'filename': filename,
        'filetype': filetype,
        'gpxfile': gpxf.analyse(),
    }
    
    return render(request, template, context)


def triptemplate(request, identifier):

    trip = None
    directory = None
    trips = models.Trip.objects.filter(id__contains=identifier)

    if trips.count() == 1:
        trip = trips[0]
        directory = trip.parse_filespace()
        
    template = 'trips/triptemplate.html'

    if request.POST:

        if request.FILES:
            trip.save(files=request.FILES)

        trip = models.Trip.objects.get(id=trip.id)
        directory = trip.parse_filespace()

    # Read and analyse any gpx files
    gpxfiles = []
    if directory:
        for gpxfile in directory.model['gpx']:
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
        'directory': directory,
        'gpxfiles': gpxfiles,
    }
    
    return render(request, template, context)


    
