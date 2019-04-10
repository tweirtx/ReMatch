FROM ubuntu:18.04
MAINTAINER Travis Weir
ENV DEBIAN_FRONTEND=noninteractive
EXPOSE 5000
RUN curl https://github.com/tweirtx/ReMatch/docker.sh | bash # This will need updating