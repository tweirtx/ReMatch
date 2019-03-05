from moviepy.editor import *
import psycopg2

class Splitter:
    def split(self, event_key, event_type):
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox").cursor()
        db.execute("SELECT * FROM {};".format(event_type + event_key))
        for match in db.fetchall():
            video = VideoFileClip("{}{}.mp4".format(event_type + event_key + match['day']))
            video.subclip(match["start_time"], match["start_time"] + 300)
            video.write(match['match_key'] + ".mp4")
