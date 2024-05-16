# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os
import glob
directory = 'uploads/files'

from flask import Flask, render_template, request, render_template_string

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

@app.route('/compute_netscan', methods=['GET','POST'])
def compute_netscan():
    try:
        cmd_1 = f'tshark -n -r uploads/files/*.pcap -q -z conv,ip > tmp'
        os.system(cmd_1)
        f = open('tmp', 'r')
        result = f.read()
        f.close()
        os.remove('tmp')
        files = glob.glob(directory + "/*")
        for f in files:
            os.remove(f)
        print(result)
        return render_template('index.html', data = result)
    except:
        result = "Err compute_netscan"
        return render_template('index.html', data = result)

@app.route('/compute_malware', methods=['GET','POST'])
def compute_malware():
        cmd_2 = f'yara -w rules/index.yar -m -a 10 -f uploads/files > tmp'
        os.system(cmd_2)
        cmd_3 = f'yara -w rules/malware_index.yar -m -a 10 -f uploads/files >> tmp'
        os.system(cmd_3)
        cmd_4 = f'sort tmp | uniq'
        f = open('tmp', 'r')
        result = f.read()
        f.close()
        os.remove('tmp')
        files = glob.glob(directory + "/*")
        for f in files:
            os.remove(f)
        print(result)
        return render_template('index.html', data = result)   
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
