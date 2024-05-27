#!/usr/bin/python3
"""The states module"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from werkzeug.exceptions import BadRequest, MethodNotAllowed


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def method_router(state_id=None):
    """A specifier for the request method"""
    specifier = {
        'GET': get_states,
        'POST': add_state,
        'PUT': modify_state,
        'DELETE': delete_state
    }
    if request.method in specifier:
        return specifier[request.method](state_id)
    else:
        raise MethodNotAllowed(list(specifier.keys()))


def get_states(state_id=None):
    """Return all states or a single state using its id"""
    states = storage.all(State).values()
    if state_id:
        res = [state for state in states if state.id == state_id]
        if res:
            return jsonify(res[0].to_dict())
        abort(404)
    states = list(map(lambda x: x.to_dict(), states))
    return jsonify(states)


def delete_state(state_id=None):
    """Deletes a state"""
    states = storage.all(State).values()
    state_to_delete = [state for state in states if state.id == state_id]
    if state_to_delete:
        storage.delete(state_to_delete[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise abort(404)


def add_state(state_id=None):
    """Adds a new state"""
    body = request.get_json()
    if type(body) is not dict:
        raise BadRequest(description='Not a JSON')
    if "name" not in body:
        raise BadRequest(description='Missing name')
    new_state = State(**body)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


def modify_state(state_id=None):
    """Updates a state information"""
    states = storage.all(State).values()
    the_state = [state for state in states if state.id == state_id]
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
