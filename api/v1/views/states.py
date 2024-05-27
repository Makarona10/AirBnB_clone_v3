#!/usr/bin/python3
"""The states module"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed
 

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def method_router(state_id=None):
    """A handler for the request method"""
    redirector = {
        'GET': get_states,
        'POST': add_state,
        'PUT': update_state,
        'DELETE': remove_state
    }
    if request.method in redirector:
        return redirector[request.method](state_id)
    else:
        raise MethodNotAllowed(list(redirector.keys()))


def get_states(state_id=None):
    """Return all states or a single state using its id"""
    all_states = storage.all(State).values()
    if state_id:
        res = [state for state in all_states if state.id == state_id]
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def remove_state(state_id=None):
    """Deletes a state"""
    all_states = storage.all(State).values()
    res = [state for state in all_states if state.id == state_id]
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise abort(404)


def add_state(state_id=None):
    """Adds a new state"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


def update_state(state_id=None):
    """Updates a state information"""
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = [state for state in all_states if state.id == state_id]
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return make_response(jsonify(old_state.to_dict()), 200)
    abort(404)