#!/usr/bin/python3
"""The states module"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from werkzeug.exceptions import NotFound
 

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    all_states = storage.all(State).values()

    if state_id:
        res = [state for state in all_states if state.id == state_id]
        if res:
            return jsonify(res[0].to_dict())
        abort(404)

    all_states_dict = [state.to_dict() for state in all_states]
    return jsonify(all_states_dict)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    states = storage.all(State).values()
    stateObj = [state for state in states if state.id == state_id]
    if stateObj:
        storage.delete(stateObj[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    body = request.get_json(force=True)
    if type(body) is not dict:
        return make_response(jsonify({"error": "Not JSON"}), 400)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing a name"}), 400)
    state = State(**body)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


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
    state = State(**state)
    state.save()
    return make_response(jsonify(state.to_dict()))
