# Installing ReMatch on Windows

## Download ReMatch
Either open a terminal and run `git clone https://github.com/tweirtx/ReMatch` or download and extract the ZIP on the GitHub website

## Installing necessary system programs
ReMatch requires certain system programs to function. Please install the following:
* [PostgreSQL](https://postgresql.org/download/windows)
* [Python 3](https://www.python.org/downloads/windows/)
* [ffmpeg](https://ffmpeg.org/download.html#build-windows)

Make sure you check the "Add Python 3.7 to PATH" option when installing Python.

Install the PostgreSQL Server and Command Line Tools when installing PostgreSQL. Leave the port field as 5432, and the rest
of the options can be changed to whatever suits your needs.

Extract ffmpeg somewhere on your system and add the bin folder to your environment variables.
See [here](https://docs.alfresco.com/4.2/tasks/fot-addpath.html) for details on adding to the PATH.

## Configure postgres
Open the SQL Shell from the Postgres Start Menu entry. Hit enter until you get a prompt that says
`postgres=#`.

Copy and paste the following into the prompt (right click the shell window to paste):
```
CREATE DATABASE rematch;
CREATE ROLE rematch;
ALTER ROLE rematch PASSWORD 'matchbox';
ALTER ROLE rematch LOGIN;
```
Exit the prompt by typing `\q` and pressing enter.

## Install Python dependencies
Open a command prompt and `cd` to your ReMatch directory. Run `pip install -Ur requirements.txt` to install dependencies.


