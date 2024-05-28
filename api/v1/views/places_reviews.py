#!/usr/bin/python3
"""Places module"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places')
def get_places_of_city(city_id):
    """Retrieves all places of a city"""
    if storage.get("City", city_id) is None:
        abort(404)
    all = storage.all("Place").values()
    places = [place.to_dict() for place in all if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """Add place to a city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_id = body.get("user_id", None)
    if not user_id:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    name = body.get("name", None)
    if not name:
        return make_response(jsonify({"error": "Missing name"}), 400)

    keys_to_remove = ["id", "created_at", "updated_at"]
    body = {k: v for k, v in body.items() if k not in keys_to_remove}
    body.update({'city_id': city_id})

    if storage.get("User", user_id) is None:
        abort(404)
    for place in storage.all("Place").values():
        if place.name == name and place.user_id == user_id:
            [setattr(place, key, value) for key, value in body.items()]
            place.save()
            return jsonify(place.to_dict()), 200

    place = Place(**body)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def manipulate_place(place_id):
    """Gets or modify or delete a place"""

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if request.method == "PUT":
        body = request.get_json(silent=True)
        if not body:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        keys_to_remove = ["id", "created_at", "updated_at", "user_id", "city_id"]
        body = {k: v for k, v in body.items() if k not in keys_to_remove}
        [setattr(place, key, value) for key, value in body.items()]
        place.save()

    if request.method == "DELETE":
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify(place.to_dict()), 200)