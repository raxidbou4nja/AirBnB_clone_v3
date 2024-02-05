#!/usr/bin/python3
'''
    RESTful API actions for State objects
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_all_states():
    '''
        Retrieve all State objects
    '''
    state_list = []
    for state in storage.all('State').values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    '''
        Retrieve one State object
    '''
    try:
        state = storage.get('State', state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)

