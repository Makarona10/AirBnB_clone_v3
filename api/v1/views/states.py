#!/usr/bin/python3
"""The states module"""


from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    body = request.get_json(force=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    storage.new(body)
    storage.save()
    return make_response(jsonify(body.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def modify_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    body = request.get_json(force=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k in body.keys():
        if k not in ["id", "created_at", "updated_at"]:
            continue
        else:
            state[k] = body[k]
    storage.save()
    return make_response(jsonify(state.to_dict()))
