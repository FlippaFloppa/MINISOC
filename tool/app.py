# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os

from flask import Flask, render_template, request, render_template_string

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def upload():
    filename = request.args.get('filename')
    cmd = f'tcpreplay -K --pps=10000 -i eth0 uploads/{filename} > tmp'
    os.system(cmd)
    f = open('tmp', 'r')
    result = f.read()
    f.close()
    return render_template('index.html', data = result)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
