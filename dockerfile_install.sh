#!/usr/bin/env bash
docker pull tweirtx/rematch
docker container rename $(docker start $(docker container create tweirtx/rematch)) rematch
sleep 5
docker logs rematch