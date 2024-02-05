#!/usr/bin/python3
"""views index"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models import storage
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State
from flask import jsonify


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status')
def status():
    '''Status of my API'''
    return jsonify({'status': 'ok'})


@app_views.route('/stats')
def stats():
    '''Retrieve the number of each objects by type'''
    statistics = {key: storage.count(cls) for key, cls in classes.items()}
    return jsonify(statistics)
