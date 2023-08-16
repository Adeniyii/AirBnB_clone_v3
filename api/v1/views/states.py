#!/usr/bin/python3
"""Defines all routes for the `States` entity
"""
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/states")
def get_states():
    """Returns all states in json response"""
    states = []
    states_objs = storage.all("State")
    for state in states_objs.values():
        states.append(state.to_dict())
    return jsonify(states)

