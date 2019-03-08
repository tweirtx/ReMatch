import psycopg2
import multiprocessing
import subprocess

class Splitter:
    def split(self, event_key, event_type):
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox").cursor()
        db.execute("SELECT * FROM {};".format(event_type + event_key))
        cores = multiprocessing.cpu_count()
        for match in db.fetchall():
#            video = VideoFileClip("{}{}_{}.mp4".format(event_type, event_key, match[2])).subclip(match[1], match[1] + 300).write_videofile(match[0] + ".mp4", threads=cores, ffmpeg_params="copy")
            end_time = match[1] + 300
            subprocess.call(f"ffmpeg -i {event_type}{event_key}_{match[2]}.mp4 -ss {match[1]} -to {end_time} -c copy {match[0]}.mp4", shell=True)
