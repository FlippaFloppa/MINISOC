# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os

from flask import Flask, render_template, request

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def upload():
    filename = request.args.get('filename')
    cmd = f'tcpreplay -K --pps=10000 -i eth0 uploads/{filename} > tmp' 
    os.system(cmd)
    result = (open('tmp', 'r').read())
    return render_template_string(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
