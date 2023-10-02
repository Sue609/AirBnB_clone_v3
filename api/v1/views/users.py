#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions.
"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_list_of_users():
    """
    Retrieves the list of all User objects: GET /api/v1/users
    """
    user = storage.all(User)
    user_list = [user.to_dict() for user in user.values()]
    return jsonify(user_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_a_user(user_id):
    """
    Retrieves a User object: GET /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_user(user_id):
    """
    Deletes a User object:: DELETE /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_object_user():
    """
    Creates a User: POST /api/v1/users
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    json_object = request.get_json()
    new_user = User(**json_object)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_object_user(user_id):
    """
    Updates a User object: PUT /api/v1/users/<user_id>
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
