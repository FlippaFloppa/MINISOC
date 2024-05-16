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
    "UPLOADED_PATH" : "uploads/files",
    "URL_ANALYZE":"http://tool-svc:5001",
    "URL_GRAFANA": "http://prometheus-grafana:3000",
    "URL_STATS": "http://soc-svc:5000",
    "URL_CLUSTER": "http://kubernetes-dashboard-kong-proxy",
}

