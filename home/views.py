from django.shortcuts import render, redirect


def index(request):

    template = 'index.html'
    context = {
        'title': 'The title',
    }

    return render(request, template, context)
