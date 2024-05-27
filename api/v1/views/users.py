#!/usr/bin/python3
"""The users module"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves all users"""
    users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a user"""
    users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in users if obj.id == user_id]
    if not user_obj:
        abort(404)
    return jsonify(user_obj[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user"""
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users if obj.id == user_id]
    if not user:
        abort(404)
    user.remove(user[0])
    for obj in users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new user"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing name")
    if "password" not in request.get_json():
        abort(400, "Missing name")
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """Updates a User object"""
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users if obj.id == user_id]
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user[0]['first_name'] = request.json['first_name']
    except:
        pass
    try:
        user[0]['last_name'] = request.json['last_name']
    except:
        pass
    for obj in users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except:
                pass
    storage.save()
    return make_response(jsonify(user[0]), 200)
