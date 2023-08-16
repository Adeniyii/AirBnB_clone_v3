#!/usr/bin/python3
"""Defines a function"""
from flask.json import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Defines a status route returning a json object of the api status.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns all stored entities from storage"""
    from models import storage
    entities = storage.count()
    return (jsonify(entities))
