# ReMatch
An expandable event stream archive to individual match clips splitter.

## Features
* Automated splitting for FRC events.
* Multi-day support.
* Once the archive has been downloaded, the splitting operation is fast.
* Automatically organizes the clips into a folder for that event.
* Can use hosted copy (email the address on my GitHub profile for inquiries) or self-host your own.
* Easily expandable to other event types
* Can be invoked either through the command line or a nice web dashboard.
![](webdash.png)

## Installation
If you are interested in self-hosting your own copy, check out WINDOWS\_INSTALL.md if you're a Windows user and POSIX\_INSTALL.md if you are using it on Linux or macOS. These files are still a work in progress, but they will be complete soon.

## Usage
There are multiple ways to use ReMatch. The simplest is to email me at the email address listed on my GitHub profile and request a ReMatch job for your event.

If you are self-hosting, there are two ways to start a run.

### Web Control
Web control gives you a nice interface to the ReMatch backend. To start the web interface, open a terminal prompt and change to your ReMatch directory. Run `python3 web.py` to start the interface, then you can use it by browsing to localhost:5000.

### Command Line Control
Todo

## Limitations
* Only Twitch VODs are supported for the time being.
* Setup for a self-hosted instance is complicated.
* Manual input is not yet an option, however it will be soon.
* Only 3 max videos are supported at a time.

## To Be Implemented
* Manual entry
* Support for YouTube archives
* Flexible amount of videos
* Intro addition to all clips
* Queuing system
* Automatic YouTube uploading
* (FRC specific) The Blue Alliance match video suggestions
* Splitter cluster system
