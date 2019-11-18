from flask import Flask, jsonify, abort, make_response, request, url_for;
from flask_httpauth import HTTPBasicAuth;

import requests;
import json;

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

@app.route('/')
def index():
    return "Connection established";

@app.route('/api', methods=['GET'])
def get_report():
    # url_code = request.args.get('path');
    # if len(url_code) == 0:
    #     abort(404);
    print('Generating report for: ');
    api_key = '###########'
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {'client': {'clientId': "mycompany", 'clientVersion': "0.1"},
            'threatInfo': {'threatTypes': ["SOCIAL_ENGINEERING", "MALWARE"],
                            'platformTypes': ["ANY_PLATFORM"],
                            'threatEntryTypes': ["URL"],
                            'threatEntries': [{'url': "textspeier.de"}]}}
    params = {'key': api_key}
    r = requests.post(url, params=params, json=payload)
    # Print response
    print(r)
    print(r.json())
    # Print response
    return jsonify({'report': 'completed'});

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Request not found'}), 404);

if __name__ == '__main__':
    app.run(debug=True);
