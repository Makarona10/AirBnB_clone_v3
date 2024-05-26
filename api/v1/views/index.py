#!/usr/bin/python3
"""The index file for views of the project"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def get_status():
    """Return the status of api"""
    return make_response(jsonify({"status": "OK"}))

@app_views.route('/stats')
def get_count():
    """Returns number of objects"""
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for k, val in objects.items():
        objects[k] = storage.count(val)
    return make_response(jsonify(objects))