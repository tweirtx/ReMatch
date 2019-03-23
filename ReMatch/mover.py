import os
import argparse
import subprocess

class Mover:
    def move(event_key):
        os.mkdir("public/" + event_key)
        if os.name == 'nt':
            subprocess.call(f"move {event_key}_* public/{event_key}", shell=True)
        elif os.name == 'posix':
            subprocess.call(f'mv {event_key}_* public/{event_key}', shell=True)
        else:
            print("I don't know how to deal with {}, exiting!".format(os.name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_key")
    key = parser.parse_args()
    Mover.move(key.event_key)
