#!/usr/bin/env bash
docker pull tweirtx/rematch
docker logs $(docker start $(docker container create tweirtx/rematch) && sleep 5)