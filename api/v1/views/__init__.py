"""Initializes main blueprint for flask application"""
from flask import Blueprint

app_views = Blueprint("site", __name__)
from api.v1.views.index import *  # noqa
from api.v1.views.states import *  # noqa
from api.v1.views.cities import *  # noqa
from api.v1.views.amenities import *  # noqa
