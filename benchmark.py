import datetime
import subprocess

start_time = datetime.datetime.now().timestamp()

# subprocess.call("python3 -m ReMatch 403531726 twitch 2019txdls frc 404054759 twitch 404158536 twitch", shell=True)
subprocess.call("python3 -m ReMatch", shell=True)

print("This benchmark run took {} seconds to complete".format(datetime.datetime.now().timestamp() - start_time))
