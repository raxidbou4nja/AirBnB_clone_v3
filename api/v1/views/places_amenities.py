#!/usr/bin/python3
""" Places Amenities view """
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_places_amenities(place_id):
    """ Handle amenities for a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    elif request.method == 'POST':
        amenities = storage.all(Amenity)
        place_amenities = place.amenities

        for amenity_id, amenity in amenities.items():
            if amenity_id in place_amenities:
                return jsonify(amenity.to_dict()), 200

        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def handle_place_amenity(place_id, amenity_id):
    """ Handle amenities for a place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if amenity_id not in place.amenities:
            abort(404)

        place.amenities.remove(amenity_id)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'POST':
        if amenity_id in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
