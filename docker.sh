#!/usr/bin/env bash
apt update && apt dist-upgrade -y && apt install ffmpeg curl postgresql-10 make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git sudo python3-pip libpq-dev -y
git clone https://github.com/tweirtx/ReMatch
python3 -m pip install -Ur ReMatch/requirements.txt
adduser rematch
sudo service postgresql restart
chmod 777 ReMatch &&
cd ReMatch
sudo -u rematch python3 web.py