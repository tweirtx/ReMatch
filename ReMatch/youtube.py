import dateutil.parser
from googleapiclient.discovery import build
import google
from google.oauth2 import credentials

CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_broadcast(broadcast_id):
    try:
        user_credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('youtube_oauth.json')
    except FileNotFoundError:
        print("You must authenticate with YouTube from the web portal first!")
        return exit(1)
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=user_credentials)
    time = youtube.videos().list(part="liveStreamingDetails", id=broadcast_id).execute().get('items')[0]['liveStreamingDetails']['actualStartTime']
    return dateutil.parser.parse(time)
