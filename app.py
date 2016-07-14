from flask import Flask, request, session, g, redirect, url_for, render_template, jsonify
import json
import os
from collections import Counter

app = Flask(__name__)
json_data = {}

@app.route('/')
def home():
    return render_template('test.html')

@app.route('/data', methods=['GET'])
def data():
    return jsonify(json_data)

@app.route('/yearly', methods=['GET'])
def yearly():
    # for x in json.keys()
    # return str(sorted([json_data[x]['Date']['Year'] for x in json_data.keys()]))

    yearly = { y : Counter([json_data[x]['Brand'] for x in json_data.keys() if json_data[x]['Date']['Year'] == y]) for y in range(1994,2016) }
    # for x in yearly:


    return jsonify(yearly)

if __name__ == '__main__':
    global json_data
    with open('cleaned_data.json', 'r') as fp:
        json_data = json.load(fp)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
