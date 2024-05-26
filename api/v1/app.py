#!/usr/bin/python3
"""The app module"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv


HOST = getenv('HBNB_API_HOST', '0.0.0.0')
PORT = int(getenv('HBNB_API_PORT', '5000'))
app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def tear_it_down(e):
    """Teardown flask app"""
    storage.close()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
