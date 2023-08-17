#!/usr/bin/python3
"""Defines all routes for the `Place` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """Returns all places linked to given city_id"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        return abort(404)
    places = city_obj.places
    if places is None:
        return abort(404)
    place_objs = []
    for place in places:
        place_objs.append(place.to_dict())
    return jsonify(place_objs)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Returns place with given place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route("cities/<city_id>/places/", methods=["POST"])
def create_place(city_id):
    """Creates a new place in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    if "user_id" not in data:
        return abort(400, description="Missing user_id")

    city = storage.get("City", city_id)
    user = storage.get("User", data.get("user_id"))
    if city is None or user is None:
        return abort(404)

    place = classes["Place"](**data)
    city.places.append(place)
    city.save()
    place.__delattr__("city")
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place object from storage"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a place object by id"""
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
