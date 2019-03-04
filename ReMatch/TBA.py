import tbapi
import psycopg2

class TBA():
    def DB_setup(self, event_key, day_one_timestamp, day_two_timestamp, day_three_timestamp, event_type):
      tablestring = "match_key text PRIMARY KEY NOT NULL, start_time int8 NOT NULL, day text NOT NULL".format(event_key)
      with open('tbakey.txt', 'r') as key:
          client = tbapi.TBAParser(key.readline().strip("\n"), cache=False)
      db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox").cursor()
      create_string = "CREATE TABLE {}{} ({})".format(event_type, event_key, tablestring)
      db.execute(create_string)
      matches = client.get_event_matches(event_key) # Todo once I have the right method available
      for match in matches:
            time = match['actual_time']
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
            datastring = '"{}", {}, "{}"'.format(match['key'], start_time, day)
      db.execute("INSERT INTO {} VALUES ({})".format(event_type + event_key, datastring))
      db.commit()
# DB Schema: String match_key, int start_time, String day
