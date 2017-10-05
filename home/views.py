from django.shortcuts import render, redirect

import gpxpy

import trips.forms
import trips.models as models

def index(request):

    template = 'index.html'
    context = {
        'title': 'The title',

        'trips': trips.models.Trip.objects.all(),
    }

    #trip = models.Trip.objects.get(id='b1ee6b0c-cb33-433d-b658-2ae1ea4a2d8f')

    if request.POST:

        s = models.GPXFile(request.FILES['gpx'], trip=trip)
        for warning in s.warnings:
            print warning

                            
        
    return render(request, template, context)
