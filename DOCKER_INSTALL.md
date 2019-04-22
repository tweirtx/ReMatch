#Docker-based setup
Docker is the recommended method to set up your ReMatch environment, especially on POSIX systems.
Setup is extremely simple and, assuming Docker is installed correctly, is guaranteed to work.

## Before you continue
This step should be obvious. Install Docker from [this link](https://docs.docker.com/install/) based on the instructions
for your OS.

## Linux/MacOS

### Run my setup script
You, my friend, have a shortcut. Run ```curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/dockerfile_install.sh | bash```

## Windows
I haven't mastered the art of Powershell scripting yet, so here's a manual guide to tide y'all over before I try it.

### Download my Docker image
Run ```docker pull tweirtx/rematch``` to download my Docker image. 

### Provision the container
Run ```docker container create tweirtx/rematch``` to create a container using the ReMatch image. It will spit out a hash,
please highlight it and hit ```CTRL-SHIFT-C``` to copy it.

### Start the container
Type ```docker run``` and right-click your terminal to paste in the hash you copied in the last step. 