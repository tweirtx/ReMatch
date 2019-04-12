#!/usr/bin/env bash
apt update && apt dist-upgrade -y && apt install ffmpeg postgresql-10 git sudo python3 -y
git clone https://github.com/tweirtx/ReMatch
python3 -m pip install -Ur ReMatch/requirements.txt
adduser rematch --disabled-password --gecos ""
sudo service postgresql restart
chmod 777 ReMatch