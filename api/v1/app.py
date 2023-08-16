#!/usr/bin/python3
"""Instantiates the flask application"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(f):
    """cleanup function"""
    storage.close()
    return f


if __name__ == "__main__":
    app.run(
        os.getenv('HBNB_API_HOST', '0.0.0.0'),
        int(os.getenv('HBNB_API_PORT', 5000)),
        threaded=True
    )
