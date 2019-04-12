FROM ubuntu:18.04
MAINTAINER Travis Weir
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 5000
RUN apt update
RUN apt install curl -y
RUN curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/docker.sh | bash
RUN sudo -u rematch python3 web.py