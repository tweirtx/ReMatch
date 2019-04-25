import tbapi
import psycopg2
import datetime
import time as libtime


class TBA:
    def DB_setup(self, event_key, day_one_timestamp, day_two_timestamp, day_three_timestamp, event_type):
        tablestring = "match_key text PRIMARY KEY NOT NULL, start_time int8 NOT NULL, day text NOT NULL"
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
            if day_two_timestamp is not None and day_three_timestamp is not None:
                if time < day_two_timestamp:
                    day = "one"
                    start_time = time - day_one_timestamp
                elif day_two_timestamp < time < day_three_timestamp:
                    day = "two"
                    start_time = time - day_two_timestamp
                else:
                    day = "three"
                    start_time = time - day_three_timestamp
            elif day_two_timestamp is not None:
                if time < day_two_timestamp:
                    day = "one"
                    start_time = time - day_one_timestamp
                else:
                    day = "two"
                    start_time = time - day_two_timestamp
            else:
                day = "one"
                start_time = time - day_one_timestamp
            datastring = "'{}', {}, '{}'".format(match['key'], start_time, day)
            db.execute("INSERT INTO {} (match_key, start_time, day) VALUES ({});".format(event_type + event_key, datastring))
        db.execute("COMMIT;")
