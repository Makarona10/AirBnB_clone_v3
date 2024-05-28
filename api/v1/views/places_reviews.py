#!/usr/bin/python3
"""Places module"""
from flask import abort, jsonify, request, from flask import abort, jsonify, request, make_response

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
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    user_id = body.get('user_id', None)
    if not user_id:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    name = body.get('name', None)
    if not name:
        return make_response(jsonify({'error': "Missing name"}), 400)

    body.pop('id', None)
    body.pop('created_at', None)
    body.pop('updated_at', None)
    body.update({'city_id': city_id})

    if storage.get("User", user_id) is None:
        abort(404)
    # this place already exists. Just update place with new data
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
    """GET/UPDATE/DELETE place object based off id else raise 400"""

    place = storage.get("Place", place_id)  # Get place
    if not place:
        abort(404)

    if request.method == 'PUT':  # Update place
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': "Not a JSON"}), 400

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('user_id', None)
        data.pop('city_id', None)

        # update attributes
        [setattr(place, key, value) for key, value in data.items()]
        place.save()

    if request.method == 'DELETE':  # Delete place
        place.delete()
        storage.save()
        return jsonify({}), 200  # DELETE method

    return jsonify(place.to_dict()), 200  # GET, PUT method