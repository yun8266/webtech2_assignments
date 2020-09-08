import os
import json
import random
import base64
import time
os.environ['FLASK_ENV'] ='development'

from flask import Flask,request,make_response,send_file

inital_data = {
    "Topics": [
        {
            "Name": "Computer Science",
            "Abbr": "CSE",
            "seats": 500
        },
        {
            "Name": "Electronics and Communication Engineering",
            "Abbr": "ECE",
            "seats": 4
        },
        {
            "Name": "Electrical and Electronics Engineering",
            "Abbr": "EEE",
            "seats": 500
        },
        {
            "Name": "Mechanincal Engineering",
            "Abbr": "ME",
            "seats": 0
        },
        {
            "Name": "Biotech",
            "Abbr": "BT",
            "seats": 500
        }
    ],
    "Selection":{}
}

app =Flask("seatserver",static_folder=os.getcwd(),static_url_path='/')

# Load all data from data.json
def load_data():
    f = open("data.json")
    data = json.load(f)
    f.close()
    return data

# Save data into data.json
def save_data(data):
    f = open("data.json",'w')
    json.dump(data,f,indent=4)
    f.close()

if not os.path.exists("data.json"):
    save_data(inital_data)

# Make a JSON response with data as body
def json_response(data):
    resp= make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.data = json.dumps(data)
    return resp

# Simulate fallback 
# The first URL has a 30% chance to timeout
@app.before_request
def before():
    print(request.url_rule)
    if request.url_rule and "2" not in request.url_rule.rule:
        if random.random()>0.7:
            time.sleep(2)
            
@app.after_request
def after(response):
    if request.url_rule and request.url_rule.rule=="/":
        response.headers['Cache-Control'] = 'no-store'
    return response

# Index route
@app.route("/")
def index():
    return send_file('seats.html')

# Select a given branch by index 
@app.route("/select",methods=['POST'])
def select():
    data = load_data()
    body = request.get_json()
    selection = body['selection']
    name = body['name']

    if data['Topics'][selection]['seats']==0:
        return make_response("Unavailable",403)

    if name in data['Selection']:
        previous = data['Selection'][name]
        data['Topics'][previous]['seats']+=1

    data['Topics'][selection]['seats']-=1
    data['Selection'][name] = selection 
    
    resp = {
        'Topics':data['Topics'],
        'selection':selection
    }

    save_data(data)
    return json_response(resp)

# Unselect a given branch by index
@app.route("/unselect",methods=['POST'])
def unselect():
    data = load_data()
    body = request.get_json()
    name = body['name']
    selection = body['selection']
    # verify if student has indeed selected this branch
    # this will deal with requests being timed out on client not update seat count more than once
    if data['Selection'][name]==selection: 
        data['Selection'].pop(name,None)
        data['Topics'][selection]['seats']+=1
    resp = {
        'Topics':data['Topics']
    }
    save_data(data)
    return json_response(resp) 

# Get all the data
@app.route("/getall",methods=['POST'])
def getall():
    data = load_data()
    body = request.get_json()

    resp = {
        'Topics':data['Topics']
    }
    if body['name'] in data['Selection']:
        resp['selection'] = data['Selection'][body['name']]
    return json_response(resp)

# Extra routes for fallback
app.add_url_rule("/getall2",'getall',methods=['POST'])
app.add_url_rule("/select2",'select',methods=['POST'])
app.add_url_rule("/unselect2",'unselect',methods=['POST'])

app.run(debug=True,port=8080)
