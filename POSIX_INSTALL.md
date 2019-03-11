# Installing ReMatch on Linux/macOS systems
Thanks to the power of bash, the setup is two steps on your part.
## Install dependencies
Because we can't plan for every single package manager, you'll need to install these
dependencies before running the automatic setup script: 
* postgres
* ffmpeg
* curl
* [Any packages required by pyenv for your distro](https://github.com/pyenv/pyenv/wiki/Common-build-problems)

## (macOS Only) Export your PATH
Because of certain issues with macOS, we must add the psql tool to our path manually.
Please run the following command in the terminal you are running for ReMatch:
```export PATH="/Library/PostgreSQL/11/bin:$PATH"```
## Run the installer script
Copy and paste the following command into your terminal:
```curl https://raw.githubusercontent.com/tweirtx/ReMatch/master/install.sh | bash```