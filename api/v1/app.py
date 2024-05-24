#!/usr/bin/python3
"""The app module"""

from flask import Flask, make_response
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext():
    """Teardown flask app"""
    storage.close()

if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True)