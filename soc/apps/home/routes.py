# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint, costants
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import os


@blueprint.route('/index')
@login_required
def index():
    return render_template('pages/index.html', segment='index')

@blueprint.route('/typography')
@login_required
def typography():
    return render_template('pages/typography.html')

@blueprint.route('/color')
@login_required
def color():
    return render_template('pages/color.html')

@blueprint.route('/icon-tabler')
@login_required
def icon_tabler():
    return render_template('pages/icon-tabler.html')

@blueprint.route('/sample-page')
@login_required
def sample_page():
    return render_template('pages/sample-page.html')  

@blueprint.route('/cluster')
@login_required
def cluster():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_CLUSTER"]+"/#/login",
        name="Cluster"
    )  

@blueprint.route('/analyzer')
@login_required
def analyzer():
    return render_template('pages/analyzer.html')  

@blueprint.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(costants["UPLOADED_PATH"], f.filename))
    return render_template('pages/analyzer.html')

#@blueprint.route('/compute_malware', methods=['POST', 'GET'])
#@login_required
#def request_analyze():
#    response = requests.get(costants["URL_ANALYZE"]+'/compute_malware') # todo: change to the correct url
#    return render_template('pages/analyzer.html', analyze_output=response.text) 

@blueprint.route('/compute_netscan', methods=['POST', 'GET'])
@login_required
def request_analyze():
    response = requests.get(costants["URL_ANALYZE"]+'/compute_netscan') # todo: change to the correct url
    return render_template('pages/analyzer.html', analyze_output=response.text) 

@blueprint.route('/coredns')
@login_required
def coredns():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/vkQ0UHxik/coredns?orgId=1&refresh=1s&kiosk",
        name="DNS"
    )  

@blueprint.route('/compute_resources_node_kubernetes')
@login_required
def compute_resources_node_kubernetes():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/200ac8fdbfbb74b39aff88118e4d1c2c/kubernetes-compute-resources-node-pods?orgId=1&refresh=10s&var-datasource=default&var-cluster=&var-node=kubernetes&kiosk",
        name="Pods Workload - Master"
    )  

@blueprint.route('/compute_resources_node_worker')
@login_required
def compute_resources_node_worker():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/200ac8fdbfbb74b39aff88118e4d1c2c/kubernetes-compute-resources-node-pods?orgId=1&refresh=10s&kiosk",
        name="Pods Workload - Worker"
    )  

@blueprint.route('/persistent_volume')
@login_required
def persistent_volume():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/919b92a8e8041bd567af9edab12c840c/kubernetes-persistent-volumes?orgId=1&refresh=10s&kiosk",
        name="Volumes"
    )  

@blueprint.route('/networking_pod')
@login_required
def networking_pod():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/8b7a8b326d7a6f1f04244066368c67af/kubernetes-networking-namespace-pods?orgId=1&refresh=10s&kiosk",
        name="Networking"
    )  

@blueprint.route('/application_statistics')
@login_required
def application_statistics():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_STATS"]+"/stats",
        name="Application Statistics"
    )  

@blueprint.route('/trivy')
@login_required
def trivy():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/ycwPj724k/trivy-operator-dashboard?orgId=1&kiosk",
        name="Trivy Operator Dashboard"
    )

@blueprint.route('/accounts/password-reset/')
def password_reset():
    return render_template('accounts/password_reset.html')

@blueprint.route('/accounts/password-reset-done/')
def password_reset_done():
    return render_template('accounts/password_reset_done.html')

@blueprint.route('/accounts/password-reset-confirm/')
def password_reset_confirm():
    return render_template('accounts/password_reset_confirm.html')

@blueprint.route('/accounts/password-reset-complete/')
def password_reset_complete():
    return render_template('accounts/password_reset_complete.html')

@blueprint.route('/accounts/password-change/')
def password_change():
    return render_template('accounts/password_change.html')

@blueprint.route('/accounts/password-change-done/')
def password_change_done():
    return render_template('accounts/password_change_done.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500
    


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@blueprint.route('/stats', methods=['POST', 'GET'])
def stats():
    if request.method == 'GET':
        with open("templates/logs/result.html", "r") as file:
            res = file.read()
        return res

