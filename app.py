from flask import Flask
from flask import Response
from adal import AuthenticationContext
import flask
import uuid
import requests
import config

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
    login_url = 'http://localhost:{}/login'.format(PORT)

    resp = Response(status=307)
    resp.headers['location'] = login_url
    return resp


@app.route("/login")
def login():
    auth_state = str(uuid.uuid4())
    print ('Auth'+str(auth_state))
    SESSION.auth_state = auth_state
    requests.get('https://login.microsoftonline.com', auth=('sheetal@hackmay2018.onmicrosoft.com', '$RoamTheWorld11'))
   
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    print('Auth url '+str(authorization_url))
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
    print('Resp '+str(resp))
    return resp


@app.route("/getAToken")
def main_logic():
    code = flask.request.args['code']
    print ('Code'+str(code))
    state = flask.request.args['state']
    print ('State'+str(state))
    if state != SESSION.auth_state:
        raise ValueError("State does not match")
    auth_context = AuthenticationContext(AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE,
 
                                                                     config.CLIENT_ID, config.CLIENT_SECRET)
    print ('context'+str(auth_context))
    print('token'+str(token_response))
    SESSION.headers.update({'Authorization': "Bearer" + token_response['accessToken'],
                            'User-Agent': 'adal-python-sample',
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'return-client-request-id': 'false'})
    return flask.redirect('/graphcall')


@app.route('/graphcall')
def graphcall():
    endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me'
    
    graph_data = SESSION.get(endpoint,  stream=False).json()
    print ('Session'+str(graph_data))
    
    return flask.render_template('display_graph_info.html', graph_data=graph_data)


if __name__ == "__main__":
    app.run()
