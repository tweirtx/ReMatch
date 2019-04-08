FROM ubuntu:18.04
MAINTAINER Travis Weir
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt dist-upgrade -y && apt install ffmpeg curl postgresql-10 make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git sudo python3-pip libpq-dev -y
RUN curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/install.sh | bash
RUN sudo service postgresql restart
RUN python3 -m pip install -Ur ReMatch/requirements.txt
RUN cd ReMatch && python3 benchmark.py
EXPOSE 5000
RUN cd ReMatch && python3 web.py