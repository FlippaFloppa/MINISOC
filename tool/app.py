# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import os
import glob
import re
from flask import Flask, request, make_response, jsonify

directory = 'uploads/files'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/compute-netscan', methods=['GET','POST'])
def compute_netscan():
    try:
        user = request.args.get('user')
        quantity = int(request.args.get('quantity'))
        index_start = int(request.args.get('index_start'))
        filters = request.args.get('filters')
        print("filters",filters)

        filter_cmd = ""
        if filters:
            # put each element of the filters array in a string separated with " "
            filter_cmd = '-R '
            join_res= filters.replace(","," -R ")
            filter_cmd += f'{join_res} -2 '
        print("filter_cmd",filter_cmd)

        if index_start < 0:
            index_start = 0
        if quantity < 0:
             result=make_response(jsonify("Bad arguments"), 400)
             return result
            
        print(f"Returning posts from {index_start} to {index_start + quantity}")
        end = index_start + quantity
        window_cmd = "frame.number in {"+str(index_start)+".."+str(end)+"}"
        print("window_cmd",window_cmd)

        # cmd_1a = f'tshark -n -r uploads/files/asd/normal_runsomware1.pcap -Y "{window_cmd}" {filter_cmd} -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e _ws.col.Info -E header=y -E separator=, -E quote=d -E occurrence=f > tmp'
        cmd_0 = f'mergecap -w merge_tmp.pcapng {directory}/{user}/*.pcap'
        os.system(cmd_0)

        cmd_1a = f'editcap -r merge_tmp.pcapng small_tmp.pcapng {index_start}-{index_start + quantity} | tshark -n -r small_tmp.pcapng {filter_cmd} -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e _ws.col.Protocol -e _ws.col.Info -E header=y -E separator=, -E quote=d -E occurrence=f > tmp'
        
        # cmd_1a = f'tshark -n -r {directory}/{user}/normal_runsomware1.pcap -a packets:{quantity} -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e _ws.col.Info -E header=y -E separator=, -E quote=d -E occurrence=f > tmp'
        os.system(cmd_1a)
        f = open('tmp', 'r')
        result = f.read()
        f.close()
        os.remove('tmp')
        os.remove('small_tmp.pcapng')
        os.remove('merge_tmp.pcapng')

        if(result == ""):
            print("No packets found\n")
            result=make_response(jsonify("No packets found"), 400)
        result = make_response(jsonify(result), 200)
        return result
    except Exception as e: 
        print(e)
        print("Err compute_netscan\n")
        result = make_response(jsonify("Err compute_netscan"), 500)
        return result 

@app.route('/compute-malwarescan', methods=['GET','POST'])
def compute_malwarescan():
    try:
        user = request.args.get('user')
        cmd_2 = f'yara -w rules/index.yar -m -a 30 -f {directory}/{user} > tmp'
        os.system(cmd_2)
        cmd_3 = f'yara -w rules/malware_index.yar -m -a 30 -f {directory}/{user} > tmp' # todo: change to append
        os.system(cmd_3)
        cmd_4 = f'sort tmp | uniq'
        f = open('tmp', 'r')
        result = f.read()
        f.close()
        os.remove('tmp')
        result = format_yara(result)

        if(result == ""):
            print("Nothing found\n")
            result=make_response(jsonify("Nothing found"), 400)
        result = make_response(jsonify(result), 200)
        return result
    except Exception as e: 
        print(e)
        print("Err compute_malwarescan\n")
        result = make_response(jsonify("Err compute_malwarescan"), 500)
        return result 
    
def format_yara(input_text): 
    formatted_text = input_text.replace(" ,", ",").replace(", ", ",").replace("] ", ",").replace(" [", ",")
    PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
    formatted_text= PATTERN.split(formatted_text)[1::2]

    # Flatten the input data by splitting elements containing '\n'
    split_data = []
    for item in formatted_text:
        split_data.extend(item.strip().split('\n'))

    # Initialize the output list and current group
    output_data = []
    current_group = []

    # Iterate through the split data and group elements correctly
    for item in split_data:
        current_group.append(item)
        if 'uploads/files/' in item:
            output_data.append(current_group)
            current_group = []

    # Handle the case where the last group might not have been added
    if current_group:
        output_data.append(current_group)

    cleaned_data = []
    for row in output_data:
        cleaned_row = [elem for elem in row if elem]
        # given the header "Function,Author,URL,Description,File Path", place each element in the exact column
        new_cleaned_row = [''] * 5
        new_cleaned_row[0] = row[0]
        for elem in cleaned_row:
            if elem.startswith("author="):
                new_cleaned_row[1] = elem
            elif elem.startswith("url="):
                new_cleaned_row[2] = elem
            elif elem.startswith("description="):
                new_cleaned_row[3] = elem
            else:
                new_cleaned_row[-1] = elem
        # in each element replace "word=" with ""
        new_cleaned_row = [re.sub(r'\w+=', '', elem) for elem in new_cleaned_row]
        cleaned_data.append(new_cleaned_row)

    formatted_lines = [','.join(row) for row in cleaned_data]

    header = "Function,Author,URL,Description,File Path"
    formatted_lines.insert(0, header)
    
    result = '\n'.join(formatted_lines)

    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
