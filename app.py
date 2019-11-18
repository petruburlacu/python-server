from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, request, url_for;
from flask_httpauth import HTTPBasicAuth;

import sys
import requests
import json
import socket

auth = HTTPBasicAuth();
app = Flask(__name__);

## Basic authentication method to be used with requests
@auth.get_password
def get_password(username):
    if username == 'root':
        return 'python';
    return None;

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401);

tasks = [
    {
        'id': 1,
        'title': u'Action description',
        'description': u'Description of the specific action',
        'done': False
    },
    {
        'id': 2,
        'title': u'Action 2',
        'description': u'Description of the second action',
        'done': False
    }
];

def make_public_tasks(task):
    new_task = {};
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external=True);
        else: 
            new_task[field] = task[field];
    return new_task;

@app.route('/')
def index():
    return "Connection established";

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id];
    if len(task) == 0:
        abort(404);
    return jsonify({'task': task[0]});

## Improved end point example
## Ensuring that the users see uri's instead of db id's
@app.route('/api/tasks/get', methods=['GET'])
@auth.login_required
def get_tasks_new():
    return jsonify({'tasks': [make_public_tasks(task) for task in tasks]});

@app.route('/api/tasks',  methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks});

@app.route('/api/tasks', methods=['POST'])
def create_task():
    ## Error handling
    if not request.json or not 'title' in request.json:
        abort(404);
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    };
    tasks.append(task);
    return jsonify({'task': task}), 201;

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id' == task_id]];
    if len(task) == 0:
        abort(404);
    if not request.json:
        abort(404);
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(404);
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(404);
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(404);
    task[0]['title'] = request.json.get('title', task[0]['title']);
    task[0]['description'] = request.json.get('description', task[0]['description']);
    task[0]['done'] = request.json.get('done', task[0]['done']);
    return jsonify({'task': task[0]});

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id' == task_id]];
    if len(task) == 0:
        abort(404);
    tasks.remove(task[0]);
    return jsonify({'result': True});

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Request not found'}), 404);

@app.route('/api', methods=['GET'])
def get_report():
    inputs = [{'url': "http://testsafebrowsing.appspot.com/s/phishing.html"}];
    
    valid_url = 'http://testsafebrowsing.appspot.com/s/phishing.html';
    
    # url_code = request.args.get('path');
    # if len(url_code) == 0:
    #     abort(404);
    
    ## Create an import functionallity to add a csv file with a list of urls to scan.
    ## Single POST request that has list with one or multiple items.
    print('Generating report for: ');
    api_key = '############'
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {'client': {'clientId': "mycompany", 'clientVersion': "0.1"},
            'threatInfo': {'threatTypes': ["SOCIAL_ENGINEERING", "MALWARE"],
                            'platformTypes': ["ANY_PLATFORM"],
                            'threatEntryTypes': ["URL"],
                            'threatEntries': [{'url': valid_url}]}}
    params = {'key': api_key}
    # r = requests.post(url, params=params, json=payload)
    
    ip_report = socket.getaddrinfo('testsafebrowsing.appspot.com', None, socket.AF_INET6)
    print(ip_report)
    # Print response
    # return jsonify({'report': r.json()});
    return jsonify({'report': 'Stefan is sad'});

if __name__ == '__main__':
    app.run(debug=True);
