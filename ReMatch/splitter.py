import moviepy
import psycopg2

class Splitter:
    db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox").cursor()
    def split(self, event_key, event_type):
        for match in db.fetch("SELECT * FROM {};".format(event_type + event_key)):
            video = moviepy.VideoFileClip("{}{}.mp4".format(event_type + event_key + match.day))
            video.subclip(match.get("start_time"), match.get("start_time") + 300)
            video.write(match.match_key + ".mp4")
