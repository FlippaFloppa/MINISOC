# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint, costants
from flask import render_template, request, session, redirect
from flask_login import (login_required, current_user)
from jinja2 import TemplateNotFound
import requests
import os
import csv
import webbrowser

QUANTITY = 10

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
    webbrowser.open_new_tab(costants["URL_CLUSTER"]+"/#/login")
    return redirect(request.referrer)

@blueprint.route('/analyzer-network')
@login_required
def analyzer_network():
    if 'index_start' not in session:
        session['index_start'] = 0
    return render_template('pages/analyzer.html' , 
                           title="Network Analyzer", 
                           analyzer_action="compute-netscan", 
                           show_load_more=True,
                           show_filter=True
                           )  

@blueprint.route('/analyzer-malware')
@login_required
def analyzer_malware():
    return render_template('pages/analyzer.html', 
                           title="Malware Analyzer" , 
                           analyzer_action="compute-malwarescan",
                           show_load_more=False,
                           show_filter=False
                           )  

@blueprint.route('/kasm')
@login_required
def kasm():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_KASM"],
        name="Kasm",
        sidebar_section= "Security"
    ) 

@blueprint.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                path_to_save = costants["UPLOADED_PATH"]+'/'+str(current_user.username)
                if not os.path.exists(path_to_save):
                    os.makedirs(path_to_save)
                f.save(os.path.join(path_to_save, f.filename))
    return "" # otherways gives error "The view function did not return a valid response. The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a NoneType.


@blueprint.route('/clear-files')
@login_required
def clear_files():
    if request.method == 'GET':
        path_to_save = costants["UPLOADED_PATH"]+'/'+str(current_user.username)
        for f in os.listdir(path_to_save):
            os.remove(os.path.join(path_to_save, f))
    return redirect(request.referrer)

@blueprint.route('/compute-netscan', methods=['POST', 'GET'])
@login_required
def request_analyze_netscan():
    input_filter = [key.split('-')[1] for key in request.form.keys() if key.startswith('filter-')]
    #format in a string separated with commas
    input_filter = ",".join(input_filter)

    if 'index_start' not in session:
        session['index_start'] = 0
    if request.form.keys() is not None and len(request.form.keys()) > 0:
        type_req=list(request.form.keys())[-1]
        if type_req == "previous":
            if session['index_start'] < QUANTITY:
                session['index_start'] = 0
            else:
                session['index_start'] -= QUANTITY
        elif type_req == "start_analyze":
            session['index_start'] = 0
        elif type_req == "more":
            session['index_start'] += QUANTITY
        
    payload = {'index_start': session['index_start'], 'quantity': QUANTITY, 'user': current_user.username, 'filters': input_filter}
    response = requests.get(costants["URL_ANALYZE"]+'/compute-netscan', params=payload) # todo: change to the correct url
    response = response.json()
    data = csv.reader(response.splitlines(), delimiter=',')
    return render_template('pages/analyzer.html', 
                           analyze_output=data,
                           title="Network Analyzer",
                           analyzer_action="compute-netscan",
                           show_load_more=True,
                           show_filter=True,
                           ) 


@blueprint.route('/compute-malwarescan', methods=['POST', 'GET'])
@login_required
def request_analyze_malware():
    payload = {'user': current_user.username}
    response = requests.get(costants["URL_ANALYZE"]+'/compute-malwarescan', params=payload) # todo: change to the correct url
    response = response.json()
    data = csv.reader(response.splitlines(), delimiter=',')
    return render_template('pages/analyzer.html', 
                           analyze_output=data,
                           title="Malware Analyzer", 
                           analyzer_action="compute-malwarescan",
                           show_load_more=False,
                            show_filter=False,
                           ) 


@blueprint.route('/coredns')
@login_required
def coredns():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/core-dns/core-dns?orgId=1&refresh=10s&kiosk",
        name="DNS",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/compute_resources_node_kubernetes')
@login_required
def compute_resources_node_kubernetes():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/200ac8fdbfbb74b39aff88118e4d1c2c/kubernetes-compute-resources-node-pods?orgId=1&refresh=10s&var-datasource=prometheus&var-cluster=&var-node=kubernetes&kiosk",
        name="Pods Workload - Master",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/compute_resources_node_worker')
@login_required
def compute_resources_node_worker():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/200ac8fdbfbb74b39aff88118e4d1c2c/kubernetes-compute-resources-node-pods?orgId=1&refresh=10s&kiosk",
        name="Pods Workload - Worker",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/persistent_volume')
@login_required
def persistent_volume():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/919b92a8e8041bd567af9edab12c840c/kubernetes-persistent-volumes?orgId=1&refresh=10s&kiosk",
        name="Volumes",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/networking_cluster')
@login_required
def networking_cluster():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/ff635a025bcfea7bc3dd4f508990a3e9/kubernetes-networking-cluster?orgId=1&refresh=10s&kiosk",
        name="Networking",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/kubelet')
@login_required
def kubelet():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/kubelet/kubernetes-kubelet?orgId=1&refresh=10s&kiosk",
        name="Kubelet",
        sidebar_section= "Statistics"
    )  

@blueprint.route('/application_statistics')
@login_required
def application_statistics():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_STATS"]+"/stats",
        name="Application Statistics",
        sidebar_section= "Statistics"
    )  


@blueprint.route('/trivy')
@login_required
def trivy():
    return render_template(
        'pages/statistics.html', 
        url=costants["URL_GRAFANA"]+"/d/ycwPj724k/trivy-operator-dashboard?orgId=1&kiosk",
        name="Trivy Operator Dashboard",
        sidebar_section= "Security"
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

