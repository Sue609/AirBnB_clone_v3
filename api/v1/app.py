#!/usr/bin/python3
"""
This module introuduces a function
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(exception):
    """ calls method close()"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """
    Custom error handler for 404 errors.
    returns a JSON-formatted 404 status code.
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
