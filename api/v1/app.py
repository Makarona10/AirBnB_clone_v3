#!/usr/bin/python3
"""The app module"""

import os
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
PORT = os.getenv('HBNB_API_PORT', '5000')
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={'/*': {'origins': HOST}})

@app.teardown_appcontext
def tear_it_down(e):
    """Teardown flask app"""
    storage.close()


@app.errorhandler(404)
def handler_for_404(err):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
