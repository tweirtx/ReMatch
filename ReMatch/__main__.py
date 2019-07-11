import datetime
import json
import time
from .TBA import TBA
from .splitter import Splitter
import twitch
import youtube_dl
from . import youtube
from . import mover

try:
    with open('client_secret.json', 'r') as r:
        client_secret = json.loads(r.read())

except FileNotFoundError:
    client_secret = {
        'installed': {
            'client_id': "",
            'client_secret': ""
        }
    }


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
        if time.daylight == 0:
            return vodinf.get('created_at').replace(tzinfo=datetime.timezone.utc)
        else:
            return vodinf.get('created_at').replace(tzinfo=datetime.timezone.utc)

    elif type_of_vod == "youtube":
        url = "https://youtube.com/watch?v=" + id_of_vod
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if time.daylight == 0:
            processed_time = youtube.get_broadcast(id_of_vod).replace(tzinfo=datetime.timezone(
                offset=datetime.timedelta(seconds=time.timezone)))
        else:
            processed_time = youtube.get_broadcast(id_of_vod).replace(tzinfo=datetime.timezone(
                offset=datetime.timedelta(seconds=time.altzone)))
        return processed_time
    else:
        return None


def main(event_key, event_type, videos):
    for video in videos:
        video.update(timestamp=timestamp_and_dl(video.get('video_id'),
                                                video.get('video_type'),
                                                event_type + event_key + "_" + video.get('video_id') + ".mp4"))
    if event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, videos, "frc")
    # input("Press enter when ready to split")  # Debug line, please ignore
    Splitter.split(Splitter(), event_key, event_type)
    mover.Mover.move(event_key)


if __name__ == '__main__':
    with open('process_me_next.json', 'r') as f:
        str_json = f.read()
    while "}{" in str_json:
        str_json = str_json.replace('}{', '},{')
    args = json.loads(str_json)
    args['videos'] = json.loads(args['videos'])
    main(args['event_key'],
         args['event_type'],
         args['videos'])
