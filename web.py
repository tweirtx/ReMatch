import subprocess
from flask import request, Flask, send_from_directory

app = Flask("ReMatch-Web")


@app.route('/')
def front_page():
    with open('index.html', 'r') as f:
        return f.read()


@app.route('/bootstrap.css')
def css():
    return send_from_directory('.', "bootstrap.css")


@app.route("/execute", methods=['POST'])
def execute():
    args = request.form
    command = "python3 -m ReMatch " + args['video_id'] + " " + args['video_type'] + " " + args['event_key'] + " " + args['event_type']
    print(command)
    subprocess.Popen(command)
    return send_from_directory('.', 'Execute.html')
