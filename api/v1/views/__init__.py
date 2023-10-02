#!/usr/bin/python3
"""
Init file for views
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *

from api.v1.views.states import *
from api.v1.views.cities import *
<<<<<<< HEAD

from api.v1.views.users import *

from api.v1.views.places_reviews import *
=======
from api.v1.views.amenities import *
>>>>>>> a763b776d5f42c650a4a6fc4507d2f87acb24383
