import datetime
import subprocess

start_time = datetime.datetime.now().timestamp()

subprocess.call("python3 -m ReMatch 392868701 twitch 2019txsan frc 393379750 twitch", shell=True)

print("This benchmark run took {} seconds to complete".format(datetime.datetime.now().timestamp() - start_time))
