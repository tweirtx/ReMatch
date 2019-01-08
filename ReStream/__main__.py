import argparse
from .download import Downloader


def main(video_id, archive_type,  event_key, event_type):
    if archive_type == 'twitch':
        channel = ""
        url = f"https://twitch.tv/{channel}/v/{video_id}"
    elif archive_type == 'youtube':
        url = f"https://youtube.com/watch?v={video_id}"
    else:
        print("Unsupported video type!")
        return exit(1)
    Downloader.download(Downloader(), url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process match streams into individual match clips")
    parser.add_argument('video_id', help="ID of VOD or YT video")
    parser.add_argument('video_type', help="Only twitch or youtube are supported at this time, "
                                           "please specify which one the stream archive is")
    parser.add_argument('event_key', help="Put in the event key")
    parser.add_argument('event_type', help="FTC or FRC are the only ones that will be supported for the time being")
    args = parser.parse_args()
    main(args['video_id'], args['video_type'], args['event_key'], args['event_type'])
