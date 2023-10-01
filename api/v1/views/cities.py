#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions.
"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def retrieve_list_of_cities(state_id):
    """
    Retrieves the list of all City objects: GET /api/v1/states
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities_list = [obj.to_dict() for obj in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_a_city(city_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object:: DELETE /api/v1/citiess/<city_id>.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def post_object_city(state_id):
    """
    Creates a City: POST /api/v1/states
    """
    state = storage.get(State, state_id)
    if state in None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    json_object = request.get_json()
    new_city = City(**json_object)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_object_city(city_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
