#Docker-based setup
Docker is the recommended method to set up your ReMatch environment, especially on POSIX systems.
Setup is extremely simple and, assuming Docker is installed correctly, is guaranteed to work.

## Install Docker
This step should be obvious. Install Docker according to the recommended method for your OS. [Details](https://docs.docker.com/install/)

## Download my Docker image
Run ```docker pull tweirtx/rematch``` to download my image. 
## Start the container
Run ```docker start $(docker container create tweirtx/rematch)``` (not tested on Windows, probably won't work there)