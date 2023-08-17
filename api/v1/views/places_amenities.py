#!/usr/bin/python3
"""Defines all routes for the `amenity` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_amenities(place_id):
    """Returns all amenities linked to given place_id"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        return abort(404)
    amenities = place_obj.amenities
    if amenities is None:
        return jsonify([])

    amenity_objs = []
    for amenity in amenities:
        amenity_objs.append(amenity.to_dict())
    return jsonify(amenity_objs)


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Creates a new amenity in storage"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        return abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    place.save()
    delattr(amenity, "place")
    delattr(amenity, "user")
    return jsonify(amenity.to_dict()), 201


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])  # noqa
def delete_amenity(place_id, amenity_id):
    """Deletes a amenity object from storage"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None or place is None:
        return abort(404)
    if amenity not in place.amenities:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
