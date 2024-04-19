# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os

from flask_dropzone import Dropzone
from flask import Flask, render_template, request

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE = '.txt, .pcap',
    DROPZONE_MAX_FILE_SIZE=5000,
    DROPZONE_MAX_FILES=30,
    DROPZONE_PARALLEL_UPLOADS=3,  # set parallel amount
    DROPZONE_UPLOAD_MULTIPLE=True,  # enable upload multiple
)

dropzone = Dropzone(app)

@app.route('/', methods=['POST', 'GET'])
def init():
    result = ""
    return render_template('index.html', filename=result)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                result=f.filename
                print(result)
    return render_template('index.html', filename=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
