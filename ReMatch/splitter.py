import psycopg2
import multiprocessing
import subprocess


class Splitter:
    def split(self, event_key, event_type):
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox", host='127.0.0.1').cursor()
        db.execute('SELECT * FROM "{}";'.format(event_type + event_key))
        cores = multiprocessing.cpu_count()
        for match in db.fetchall():
            end_time = match[1] + 300
            print(f"Splitting {match[2]}")
            subprocess.call(f"ffmpeg -threads {cores} -loglevel quiet -i {event_type}{event_key}_{match[2]}.mp4 -ss {match[1]} "
                            f"-to {end_time} -c copy {match[0]}.mp4", shell=True)
