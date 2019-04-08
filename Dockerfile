FROM ubuntu:18.04
MAINTAINER Travis Weir
RUN sudo apt update && sudo apt dist-upgrade -y && sudo apt install ffmpeg curl postgresql-11 make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/install.sh | bash