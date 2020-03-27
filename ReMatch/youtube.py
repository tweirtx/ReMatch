"""Interface class for YouTube uploading"""
import subprocess
import os
from subprocess import Popen, PIPE
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YouTube:
    def upload(self, event_key):
        #os.listdir should lead to the public folder.
        mylist = os.listdir("public/"+ event_key)
        for x in mylist:
            print(x)
            filepath = "--file="+ "public\\" + event_key + "\\" + x 
            #print(filepath)
            #Title of video (defaults to video name in public\eventkey folder)
            filetitle = "--title=" +  x 
            #Description for youtube
            filedescription = "--description=" + x 
            #List key words for video
            filekeywords = "--keywords=" + "\""+"TBA"+"\""
            #uploads file as unlisted
            fileprivacy = "--privacyStatus=" + "unlisted"
            #triggers upload_video.py to upload video with commands
            args = ["upload_video.py", filepath, filetitle, filedescription, filekeywords, fileprivacy]
            
            p= Popen([sys.executable or 'python3'] + args)

    def create_playlist(self, event_key):
        print("TODO: Take in an event key and create a YouTube playlist from that and return the URL")
