# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        'uploadGPX': forms.UploadGPX(),
        'trips': models.Trip.objects.all(),
    }

    trip = models.Trip.objects.get(id='b1ee6b0c-cb33-433d-b658-2ae1ea4a2d8f')

    if request.POST:

        s = models.GPXFile(request.FILES['gpx'], trip=trip)
        for warning in s.warnings:
            print warning

                            
        
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

        #s = models.GPXFile(request.FILES['gpx'], trip=trip)

        if request.FILES:
            trip.save(files=request.FILES)

        trip = models.Trip.objects.get(id=trip.id)
        directory = trip.parse_filespace()
            
        #for warning in s.warnings:
        #    print warning


    context = {
        'h1': "Trip or template",
        'identifier': identifier,
        'trip': trip,
        'trips': trips,
        'uploadFile': forms.UploadFile(),
        'forms': True,
        'directory': directory,
    }
    
    return render(request, template, context)


    
