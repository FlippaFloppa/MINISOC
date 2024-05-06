# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)

costants = {
    "UPLOADED_PATH" : "uploads",
    "URL_ANALYZE":"http://tool-svc:5001",
    "URL_GRAFANA": "http://localhost:1234",
    "URL_STATS": "http://localhost:1235",
    "URL_CLUSTER": "http://localhost:1236",
}

