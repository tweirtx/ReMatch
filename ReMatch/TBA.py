import tbapi
import psycopg2
import time as libtime


class TBA:
    def DB_setup(self, event_key, videos, event_type):
        tablestring = "match_key text PRIMARY KEY NOT NULL, start_time int8 NOT NULL, video_id text NOT NULL"
        with open('tbakey.txt', 'r') as key:
            client = tbapi.TBAParser(key.readline().strip("\n"), cache=False)
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox", host="127.0.0.1").cursor()
        create_string = "CREATE TABLE {}{} ({})".format(event_type, event_key, tablestring)
        db.execute(create_string)
        matches = client.get_event_matches(event_key)
        for match in matches:
            try:
                if libtime.daylight == 0:
                    time = match['actual_time'] + libtime.timezone
                else:
                    time = match['actual_time'] + libtime.altzone
            except Exception:
                print("An error occurred when getting the match time for", match['key'])
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
                print(start_time, match['key'], time, timestamp)
            except NameError:
                print(match['key'], 'did not compute')
                continue
            datastring = "'{}', {}, '{}'".format(match['key'], start_time, video_id)
            # noinspection SqlResolve
            db.execute("INSERT INTO {} (match_key, start_time, video_id) VALUES ({});".format(event_type + event_key, datastring))
        db.execute("COMMIT;")
