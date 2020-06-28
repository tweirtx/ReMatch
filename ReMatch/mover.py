import os
import argparse
import subprocess


class Mover:
    def move(self, event_key):
        os.mkdir("public/" + event_key)
        if os.name == 'nt':
            mv = "move"
        elif os.name == 'posix':
            mv = "mv"
        else:
            print("I don't know how to deal with {}, exiting!".format(os.name))
            return
        subprocess.call(f'{mv} temp/{event_key}* public/{event_key} && cd public && zip -r {event_key}.zip {event_key}', shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_key")
    key = parser.parse_args()
    Mover().move(key.event_key)
