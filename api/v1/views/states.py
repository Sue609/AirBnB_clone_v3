#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions.
"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_list_of_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    """
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_a_state(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object:: DELETE /api/v1/states/<state_id>.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_object_state():
    """
    Creates a State: POST /api/v1/states
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    json_object = request.get_json()
    new_state = State(**json_object)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_object_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
