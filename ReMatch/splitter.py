from moviepy.editor import *
import psycopg2
import multiprocessing

class Splitter:
    def split(self, event_key, event_type):
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox").cursor()
        db.execute("SELECT * FROM {};".format(event_type + event_key))
        cores = multiprocessing.cpu_count()
        for match in db.fetchall():
            video = VideoFileClip("{}{}_{}.mp4".format(event_type, event_key, match[2]))
            video.subclip(match[1], match[1] + 300)
            video.write_videofile(match[0] + ".mp4", threads=cores)
