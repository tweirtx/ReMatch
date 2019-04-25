import dateutil.parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_broadcast(broadcast_id):
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    time = youtube.videos().list(part="liveStreamingDetails", id=broadcast_id).execute().get('items')[0]['liveStreamingDetails']['actualStartTime']
    return dateutil.parser.parse(time)
