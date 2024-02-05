#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from flask import Flask, Blueprint, jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City).values()
    state_cities = [city.to_dict() for city
                    in cities if city.state_id == state_id]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object with a given city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object with a given city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    new_city = City(state_id=state_id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object with a given city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    # Update the City object with all key-value pairs of the dictionary
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
