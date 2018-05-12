from flask import Flask
from flask import Response
from adal import AuthenticationContext
import flask
import uuid
import requests
import config

from flask import render_template,Flask,request,redirect,url_for,session,flash,escape,send_file,jsonify,json, make_response

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

SESSION = requests.Session()
PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')


@app.route("/")
def main():
    '''login_url = 'http://localhost:{}/login'.format(PORT)

    resp = Response(status=307)
    resp.headers['location'] = login_url'''
    return login()



def login():
    auth_state = str(uuid.uuid4())
    SESSION.auth_state = auth_state
   
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
        
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
 
    return resp


@app.route("/getAToken")
def main_logic():
    code = flask.request.args['code']
    
    state = flask.request.args['state']
    
    if state != SESSION.auth_state:
        raise ValueError("State does not match")
    auth_context = AuthenticationContext(AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE,config.CLIENT_ID, config.CLIENT_SECRET)

    SESSION.headers.update({'Authorization': "Bearer" + token_response['accessToken'],
                            'User-Agent': 'adal-python-sample',
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'return-client-request-id': 'false'})
                            
        
    
                            
    '''endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me/findMeetingTimes'''
    endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me/calendars'
    graph_data = SESSION.post(endpoint,stream=False ).json()
    
    
    print ('Session'+str(graph_data))
    return jsonify(graph_data)

    


if __name__ == "__main__":
    app.run()
