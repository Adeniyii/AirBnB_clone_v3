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


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Returns a state object or None if not found."""
    state = storage.get("State", state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state object from storage"""
    state = storage.get("State", state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})
