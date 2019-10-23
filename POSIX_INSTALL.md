# Installing ReMatch on Linux/macOS systems
Thanks to the power of bash, the setup is two steps on your part.

## Install dependencies
Because we can't plan for every single package manager, you'll need to install these
dependencies before running the automatic setup script: 
* postgres (note that you must use the EnterpriseDB installer on macOS)
* ffmpeg
* curl
* [Any packages required by pyenv for your distro](https://github.com/pyenv/pyenv/wiki/Common-build-problems)

## Run the installer script
Copy and paste the following command into your terminal:
```curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/install.sh | bash```
