#!/usr/bin/python3
"""The Amenities module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves all Amenities"""
    amenities = [amenity.to_dict() for amenity in
                 storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if not amenity:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity"""
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    amenity.remove(amenity[0])
    for obj in amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Creates an Amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """Updates an Amenity object"""
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return make_response(jsonify(amenity[0]), 200)
