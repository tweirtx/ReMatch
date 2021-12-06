import psycopg2
import multiprocessing
import subprocess


class Splitter:
    def split(self, event_key, event_type):
        db = psycopg2.connect(dbname="rematch", user="rematch", password="matchbox", host='127.0.0.1').cursor()
        db.execute('SELECT * FROM "{}";'.format(event_type + event_key))
        cores = multiprocessing.cpu_count()
        for match in db.fetchall():
            end_time = match[1] + 170
            print(f"Splitting {match[2]}")
            command = f"ffmpeg -threads {cores} -loglevel quiet -i {event_type}{event_key}_{match[2]}.mp4 -ss {match[1]}"\
            + f" -to {end_time} -c:v libvpx-vp9 -c:a libopus -b:v 680k -crf 33 " \
            + f"-cpu-used 2 -b:a 64k {match[0]}.webm"
            print(command)
            subprocess.call(command, shell=True)
