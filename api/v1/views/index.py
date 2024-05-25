#!/usr/bin/python3
"""The index file for views of the project"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """Return the status of api"""
    return jsonify({"status": "OK"})
