import datetime
import json
import requests
import psycopg2


class TOA:
    with open('toakey.txt', 'r') as key:
        toakey = key.readline().strip("\n")

    def DB_setup(self, event_key, videos, event_type):
        tablestring = "match_key text PRIMARY KEY NOT NULL, start_time int8 NOT NULL, video_id text NOT NULL"
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox", host="127.0.0.1").cursor()
        create_string = 'CREATE TABLE "{}{}" ({})'.format(event_type, event_key, tablestring)
        db.execute(create_string)
        response = requests.get(f"https://theorangealliance.org/api/event/{event_key}/matches",
                                headers={"X-TOA-Key": self.toakey,
                                         "X-Application-Origin": "ReMatch",
                                         "Content-Type": "application/json"}).text
        matches = json.loads(response)
        for match in matches:
            try:
                time = datetime.datetime.strptime(match['match_start_time'][:-1], "%Y-%m-%dT%H:%M:%S.%f").timestamp()
            except Exception as e:
                print("An error occurred when getting the match time for", match['match_key'])
                print(e)
                continue
            for x in range(len(videos)):
                timestamp = videos[x].get('timestamp')
                if x == (len(videos) - 1):
                    start_time = time - timestamp
                    video_id = videos[x].get('video_id')
                elif timestamp < time < videos[x + 1].get('timestamp'):
                    start_time = time - timestamp
                    video_id = videos[x].get('video_id')
                    break
            try:
                print(start_time, match['match_key'], time, timestamp)
            except NameError:
                print(match['match_key'], 'did not compute')
                continue
            datastring = "'{}', {}, '{}'".format(match['match_key'], start_time, video_id)
            # noinspection SqlResolve
            db.execute('INSERT INTO "{}" (match_key, start_time, video_id) VALUES ({});'.format(event_type + event_key, datastring))
        db.execute("COMMIT;")

    def link_clips(self, event_key, youtube_playlist_url):
        print("TODO write a method that POSTs the YouTube playlist URL to TOA")
