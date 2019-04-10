FROM ubuntu:18.04
MAINTAINER Travis Weir
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt dist-upgrade -y && apt install ffmpeg curl postgresql-10 make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git sudo python3-pip libpq-dev -y
RUN git clone https://github.com/tweirtx/ReMatch
RUN python3 -m pip install -Ur ReMatch/requirements.txt
EXPOSE 5000
RUN adduser rematch
RUN sudo service postgresql restart && sudo -u postgres psql -c "CREATE USER rematch PASSWORD 'matchbox';" && sudo -u postgres psql -c "CREATE DATABASE rematch;" && chmod 777 ReMatch && cd ReMatch && sudo -u rematch python3 benchmark.py && python3 web.py
