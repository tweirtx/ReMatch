import datetime
import subprocess

start_time = datetime.datetime.now().timestamp()

subprocess.call("python3 -m ReMatch 389172543 twitch 2019txaus frc 389710248 twitch")

print("This benchmark run took {} seconds to complete".format(datetime.datetime.now().timestamp() - start_time))
