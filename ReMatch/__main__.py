import argparse
from .TOA import TOA
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
    if event_type == 'ftc':
        TOA.DB_setup(TOA(), event_key, timestamp)
    elif event_type == 'frc':
        TBA.DB_setup(TBA(), event_key, timestamp)
    else:
        print("Unsupported event type!")
        return exit(1)
    Splitter.split(Splitter(), event_key, event_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process match streams into individual match clips")
    parser.add_argument('video_id', help="ID of VOD")
    parser.add_argument('video_type', help="Only Twitch is supported at this time. This parameter exists for future "
                                           "expansion of this module.")
    parser.add_argument('event_key', help="Put in the event key")
    parser.add_argument('event_type', help="FTC or FRC are the only ones that will be supported for the time being")
    args = parser.parse_args().__dict__
    main(args['video_id'], args['video_type'], args['event_key'], args['event_type'])
