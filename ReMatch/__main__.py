import json
from .TBA import TBA
from .splitter import Splitter
import twitch
import youtube_dl
from . import mover
#had to change .email to .email2 because it was messing with the upload_video.py
from .email2 import Emailer
from .youtube import YouTube


def timestamp_and_dl(id_of_vod, type_of_vod, filename):
    print("Downloading " + filename)
    ydl_opts = {
        'format': 'best',
        'fixup': 'never',
        'outtmpl': filename,
    }

    if type_of_vod == "twitch":
        twitch_client = twitch.TwitchClient(client_id='a57grsx9fi8ripztxn8zbxhnvek4cp')
        vodinf = twitch_client.videos.get_by_id(id_of_vod)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vodinf.get('url')])
        return vodinf.get('created_at').timestamp()
    else:
        return None


def main(event_key, event_type, videos, email):
    for video in videos:
        video.update(timestamp=int(timestamp_and_dl(video.get('video_id'),
                                                    video.get('video_type'),
                                                    event_type + event_key + "_" + video.get('video_id') + ".mp4")))
    if event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, videos, "frc")
    # input("Press enter when ready to split") # Debug line, please ignore
    Splitter.split(Splitter(), event_key, event_type)
    mover.Mover().move(event_key)
    Emailer().send_email(email, event_key)
    YouTube().upload(event_key)
    


if __name__ == '__main__':
    with open('process_me_next.json', 'r') as f:
        str_json = f.read()
    while "}{" in str_json:
        str_json = str_json.replace('}{', '},{')
    args = json.loads(str_json)
    main(args['event_key'],
         args['event_type'],
         args['videos'],
         args['email'])
