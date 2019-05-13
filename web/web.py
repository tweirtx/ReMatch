import subprocess
import json
from flask import request, Flask, send_from_directory, redirect, session, url_for
import google
import google_auth_oauthlib
from google_auth_oauthlib.flow import Flow
from google.oauth2 import credentials

app = Flask("ReMatch-Web")
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
app.secret_key = "fvuirwhgfiuawew"


@app.route('/')
def front_page():
    return send_from_directory('web', "index.html")


@app.route('/interactive.js')
def js():
    return send_from_directory('web', "interactive.js")


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    return send_from_directory('web', "execute.html")


@app.route('/bootstrap.css')
def css():
    return send_from_directory('web', "bootstrap.css")


@app.route('/darkly.min.css')
def darklycss():
    return send_from_directory('web', "darkly.min.css")


@app.route("/execute_old", methods=['POST'])
def execute_old():
    args = request.form.to_dict()
    if args['video_type_day_two'] == 'disabled':
        args['video_type_day_two'] = ''
    if args['video_type_day_three'] == 'disabled':
        args['video_type_day_three'] = ''
    command = "python3 -m ReMatch " + args['video_id_day_one'] + " " + args['video_type_day_one'] + " " + args['event_key'] + " " + args['event_type'] + " " + args['video_id_day_two'] + " " + args['video_type_day_two'] + " " + args['video_id_day_three'] + " " + args['video_type_day_three']
    subprocess.Popen(command, shell=True)
    return send_from_directory('web', 'execute.html')


@app.route('/execute_json', methods=['POST'])
def parse_json():
    vals = json.dumps(request.json)
    print(vals)
    with open('process_me_next.json', 'w') as f:
        f.write(vals)
    command = "python3 -m ReMatch"
    subprocess.Popen(command, shell=True)
    return ""
    # Insert JSON parsing here


@app.route('/set_tba_key', methods=['POST'])
def set_tba_key():
    with open('tbakey.txt', 'w') as f:
        f.write(request.args.get("key"))
    return "Key set successfully!"


@app.route('/auth')
def auth():
    if 'credentials' not in session:
        return redirect('authorize')

    # Load the credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    credentials = credentials.__dict__
    credentials['client_secret'] = credentials['_client_secret']
    credentials['client_id'] = credentials['_client_id']
    credentials['refresh_token'] = credentials['_refresh_token']

    with open('youtube_oauth.json', 'w') as f:
        f.write(json.dumps(credentials))

    return "Authentication successful"


@app.route('/authorize')
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # both an access and refresh token.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true',
        device_name='laptop',
        device_id='asdf')

    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('auth'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
