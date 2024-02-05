#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""
from flask import Flask, Blueprint, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object with a given place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())



