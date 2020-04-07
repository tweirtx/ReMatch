"""Interface class for YouTube uploading"""
import http.client as httplib
import os
import random
import sys
import time

import google_auth_oauthlib
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
from ReMatch.playlist import scopes

httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=[YOUTUBE_UPLOAD_SCOPE, "https://www.googleapis.com/auth/youtube.force-ssl"],
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
        # print(credentials)
    # print(credentials)
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


youtube = get_authenticated_service()


class YouTube:
    def upload(self, event_key):
        # os.listdir should lead to the public folder.
        mylist = os.listdir("public/" + event_key)
        upload_ids = []
        for x in mylist:
            print(x)
            filepath = "public/" + event_key + "/" + x
            # print(filepath)
            # Title of video (defaults to video name in public\eventkey folder)
            x = x[:-4]
            filetitle = x
            # Description for youtube
            filedescription = x
            # List key words for video
            filekeywords = "\"" + "TBA" + "\""
            # uploads file as unlisted
            fileprivacy = "unlisted"
            # triggers upload_video.py to upload video with commands
            args = {'file': filepath, 'title': filetitle, 'description': filedescription, 'keywords': filekeywords,
                    'privacyStatus': fileprivacy}
            upload_ids.append({"match_key": x, "video_url": "https://youtube.com/watch?v=" + self.initialize_upload(youtube, args)})
        return upload_ids

    def initialize_upload(self, yt, options):
        tags = None
        if options['keywords']:
            tags = options['keywords'].split(",")

        body = dict(
            snippet=dict(
                title=options['title'],
                description=options['description'],
                tags=tags,
                categoryId=28
            ),
            status=dict(
                privacyStatus=options['privacyStatus']
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = yt.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True)
        )

        return self.resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." % response['id'])
                        return response['id']
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
                        return None
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def create_playlist(self, event_key, video_ids):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Get credentials and create an API client
        yt = youtube

        request = yt.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": event_key,
                    "privacyStatus": "public"
                }
            }
        )
        response = request.execute()

        for video_id in video_ids:
            insert_request = yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": response['id'],
                        "resourceId": {
                            "videoId": video_id,
                            "kind": "youtube#video"
                        }
                    }
                }
            )
            insert_response = insert_request.execute()

        return "https://www.youtube.com/playlist?list=" + response['id']
