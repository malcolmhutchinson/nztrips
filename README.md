nztrips - excursion planner
---------------------------

A GeoDjango project to plan and record trips. Road trips, tramping or
cycling trips.

Plan routes and points of interest for a trip, then download these as
GPX files for use in the field. Upload GPX files collected during the
trip. Display these data on a map. Edit and share them.

Upload photographs, and correlate them with your gps tracks, writing
GPS coords into the EXIF data of the photographs. These photo
locations can then be downloaded as a gps waypoints file.

The application will hook into spatial data about New Zealand held at
Land Information NZ (LINZ), listing roads, rivers, place names and
other data. Select point locations from LINZ data as waypoints to add
to your trip plan.

Share your trip plan and record with others. Make it public, or
private to yourself and your buddies.



### nztrips does gpx

We deal in GPX files. We don't provide for translation to shapefile,
geodatabase or any other format (at least, not at this stage). We have
plans for integrating with QGIS, but those plans are quite a long way
in the future.



## Not suitable for production

This project is in the early stages of development. At the moment, I
am determing database structures and basic functionality, so don't
expect it to actually do anything. Currently, CSS styling is entirely
absent. So is any form of authentication and authorisation.



Installation
------------

This installs as a Django application. 


### Requites 'webnote'

This application leans heavily on my filesystem parser
[webnote](https://github.com/malcolmhutchinson/webnote). Webnote is
not available in repositories, so you will have to clone it from
github.


### Requires GeoDjango

If you are unfamiliar with Django, I recommend following the
[Django tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

Create a development directory:

    $ mkdir ~/dev/nztrips
    $ cd ~/dev/nztrips

Make a directory to hold the code under version control:

    $ mkdir code

Clone the code from github:

    $ git clone https://github.com/malcolmhutchinson/nztrips.git code/

Install a virtual environment. 

    $ virtualenv env

You will have to install Django, and a number of other dependencies,
into the environment:

    $ source env/bin/activate
    (env) $ pip install django


You will have to put the webnote package onto your path. I've done
this by placing a simlink in my virtual environment at

    $ ln -s ~/dev/webnote/code/webnote ~/dev/nztrips/env/lib/python2.7/site-packages/webnote

Now, run the Django development server:

    (env) $ python code/djsrv/manage.py runserver

And point your browser at localhost, port 8000:

    http://localhost:8000/


