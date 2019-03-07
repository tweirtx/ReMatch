import os
import argparse
import shutil

class Mover:
    def move(event_key):
        os.mkdir(event_key)
        for file in os.listdir('.'):
          if event_key in file:
              try:
                  shutil.move(file, event_key + "/" + file)
              except Exception:
                  print("Error moving", file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_key")
    key = parser.parse_args()
    Mover.move(key.event_key)
