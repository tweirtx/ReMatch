from .__init__ import app
import subprocess
from flask import request


@app.route('/')
def front_page():
    return app.send_static_file("index.html")


@app.route("/execute", methods=['POST'])
def execute():
    args = request.args.__dict__
    command = "python3 -m ReMatch " + args['video_id'] + " " + args['video_type'] + " " + args['event_key'] + " " + args['event_type']
    subprocess.Popen(command)
    return "Beginning split"
