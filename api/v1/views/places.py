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


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object with a given place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object with a given place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    # Update the Place object with all key-value pairs of the dictionary
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def search():
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states", [])
    city_ids = guide.get("cities", [])
    amenity_ids = guide.get("amenities", [])

    result = []

    if not state_ids and not city_ids:
        result = storage.all(Place).values()
    else:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                result.extend(place for city
                              in state.cities for place in city.places)

        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                result.extend(place for place in
                              city.places if place not in result)

    result = [place for place in result if set(amenity_ids)
              .issubset({amenity.id for amenity in place.amenities})]

    result = [storage.get(Place, place.id).to_dict() for place in result]

    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    result = [{k: v for k, v in place_dict.items()
               if k not in keys_to_remove} for place_dict in result]

    return jsonify(result)
