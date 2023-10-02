#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions.
"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_list_of_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_a_review(review_id):
    """
    Retrieves a Review object.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_object_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    json_object = request.get_json()
    json_object['place_id'] = place_id

    user = storage.get(User, json_object['user_id'])
    if user is None:
        abort(404)
    new_review = Review(**json_object)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_object_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'email', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
