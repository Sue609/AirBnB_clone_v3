#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieves_amenities():
    """
    Retrieves a list of all amenities
    """
    all_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def retrieves_amenity(amenity_id):
    """
    retrieves an amenity using amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity in None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    delete amenity using amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_an_object_amenity(amenity_id):
    """
    creates amenity using amenity_id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_object = request.get_json()
    new_amenity = Amenity(**json_object)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Updates amenity object using amenity_id
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
