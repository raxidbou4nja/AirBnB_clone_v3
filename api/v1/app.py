#!/usr/bin/python3
"""app module"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False


app.register_blueprint(app_views)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Cleanup operations"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
