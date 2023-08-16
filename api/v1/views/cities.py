#!/usr/bin/python3
"""Defines all routes for the `City` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/cities", methods=["GET"])
def get_cities():
    """Returns all cities in json response"""
    cities = []
    cities_objs = storage.all("City")
    for city in cities_objs.values():
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/", methods=["POST"])
def create_city():
    """Creates a new city in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    city = classes["City"](**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Returns a city object or None if not found."""
    city = storage.get("City", city_id)
    return jsonify(city.to_dict()) if city else abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a city object from storage"""
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Update a city object by id"""
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
