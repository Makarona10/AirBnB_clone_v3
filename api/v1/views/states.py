#!/usr/bin/python3
"""The states module"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from werkzeug.exceptions import BadRequest
 

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    all_states = storage.all(State).values()

    if state_id:
        res = list(filter(lambda x: x.id == state_id, all_states))
        if res:
            return jsonify(res[0].to_dict())
        abort(404)

    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


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
        raise BadRequest(description="Not a JSON")
    if "name" not in body:
        raise BadRequest(description="Missing name")
    state = State(**body)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def modify_state(state_id=None):
    """Update a state"""
    all_states = storage.all(State).values()
    the_state = [state for state in all_states if state.id == state_id]
    if the_state:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = the_state[0]
        for k, val in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(old_state, k, val)
        old_state.save()
        return make_response(jsonify(old_state.to_dict()), 200)
    abort(404)
