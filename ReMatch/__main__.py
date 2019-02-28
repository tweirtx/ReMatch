import argparse
from .TBA import TBA
from .splitter import Splitter
import twitch
import youtube_dl
from pytube import YouTube


def main(video_id, archive_type,  event_key, event_type):
    if archive_type == 'twitch':
        twitch_client = twitch.TwitchClient()
        vodinf = twitch_client.videos.get_by_id(video_id)
        ydl_opts = {
            'format': 'best',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vodinf.get('url')])
        timestamp = vodinf.get('created_at')
    else:
        print("Unsupported video type!")
        return exit(1)
    if event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, timestamp, day2timestamp, day3timestamp)
    else:
        print("Unsupported event type!")
        return exit(1)
    Splitter.split(Splitter(), event_key, event_type)

def timestamp_and_dl(id, type):
    if type == "twitch":
        twitch_client = twitch.TwitchClient()
        vodinf = twitch_client.videos.get_by_id(video_id)
        ydl_opts = {
            'format': 'best',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([vodinf.get('url')])
        return vodinf.get('created_at')
    else:
        return None

def main_rewrite(event_key, event_type, day_one_id, day_one_type, day_two_id, day_two_type, day_three_id, day_three_type):
    day_one_timestamp = timestamp_and_dl(day_one_id, day_one_type)
    day_two_timestamp = timestamp_and_dl(day_two_id, day_two_type)
    day_three_timestamp = timestamp_and_dl(day_three_id, day_two_type)
    if event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, timestamp, day2timestamp, day3timestamp)
    Splitter.split(Splitter(), event_key, event_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process match streams into individual match clips")
    parser.add_argument('video_id_day_one', help="ID of VOD")
    parser.add_argument('video_type_day_one', help="Only Twitch is supported at this time. This parameter exists for future "
                                           "expansion of this module.")
    parser.add_argument('event_key', help="Put in the event key")
    parser.add_argument('event_type', help="FRC is the only ones that will be supported for the time being, this "
                                           "exists for future expansion of this module")
    parser.add_argument('video_id_day_two', help="Optional argument for multiple day support", optional=True)
    parser.add_argument('video_type_day_two', help="Optional argument for multiple day support", optional=True)
    parser.add_argument('video_id_day_three', help="Optional argument for multiple day support", optional=True)
    parser.add_argument('video_type_day_three', help="Optional argument for multiple day support", optional=True)
    args = parser.parse_args().__dict__
    main_rewrite(args['event_key'], args['event_type'], args['video_id_day_one'], args['video_type_day_one'], args['video_id_day_two'], args['video_type_day_two'], args['video_id_day_three'], args['video_type_day_three'])
