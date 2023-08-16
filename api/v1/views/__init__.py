""""""
from flask import Blueprint

app_views = Blueprint("site", __name__)
from api.v1.views.index import *  # noqa
