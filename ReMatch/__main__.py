import argparse
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
        return vodinf.get('created_at').timestamp()

    elif type_of_vod == "youtube":
        url = "https://youtube.com/watch?v=" + id_of_vod
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        broadcast_time = youtube.get_broadcast(id_of_vod).timestamp()
        if time.daylight == 0:
            processed_time = time.timezone + broadcast_time
        else:
            processed_time =  + time.altzone + broadcast_time
        return processed_time
    else:
        return None


def main(event_key, event_type, day_one_id, day_one_type, day_two_id, day_two_type, day_three_id, day_three_type):
    day_one_timestamp = timestamp_and_dl(day_one_id, day_one_type, event_type + event_key + "_one.mp4")
    day_two_timestamp = timestamp_and_dl(day_two_id, day_two_type, event_type + event_key + "_two.mp4")
    try:
        day_three_timestamp = timestamp_and_dl(day_three_id, day_three_type[0], event_type + event_key + "_three.mp4")
    except IndexError:
        day_three_timestamp = None
    if event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, day_one_timestamp, day_two_timestamp, day_three_timestamp, "frc")
#    input("Press enter when ready to split") # Debug line, please ignore
    Splitter.split(Splitter(), event_key, event_type)
    mover.Mover.move(event_key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process match streams into individual match clips")
    parser.add_argument('video_id_day_one', help="ID of Twitch VOD or YouTube stream archive")
    parser.add_argument('video_type_day_one', help="Only Twitch or YouTube are supported at this time."
                                                   " This parameter exists for future expansion of this module.")
    parser.add_argument('event_key', help="Put in the event key")
    parser.add_argument('event_type', help="FRC is the only ones that will be supported for the time being, this "
                                           "exists for future expansion of this module")
    parser.add_argument('video_id_day_two', help="Optional argument for multiple day support", nargs='?')
    parser.add_argument('video_type_day_two', help="Optional argument for multiple day support", nargs='?')
    parser.add_argument('video_id_day_three', help="Optional argument for multiple day support", nargs='?')
    parser.add_argument('video_type_day_three', help="Optional argument for multiple day support", nargs='*')
    args = parser.parse_args().__dict__
    main(args['event_key'],
         args['event_type'],
         args['video_id_day_one'],
         args['video_type_day_one'],
         args['video_id_day_two'],
         args['video_type_day_two'],
         args['video_id_day_three'],
         args['video_type_day_three'])
