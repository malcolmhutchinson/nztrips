from django.shortcuts import render, redirect

import gpxpy

import trips.forms
import trips.models as models

def index(request):

    template = 'index.html'
    context = {
        'title': 'NZ Trips, adventure trip planning and recording.',

        'trips': models.Trip.objects.all(),
    }

    return render(request, template, context)
