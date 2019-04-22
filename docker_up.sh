#!/usr/bin/env bash
docker pull tweirtx/rematch
docker container rename $(docker run -d -p 5000:5000 tweirtx/rematch) rematch
sleep 5
echo "Container is now up, and can be accessed at http://localhost:5000"
