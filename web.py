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
    args = request.form.to_dict()
    if args['video_type_day_two'] == 'disabled':
        args['video_type_day_two'] = ''
    if args['video_type_day_three'] == 'disabled':
        args['video_type_day_three'] = ''
    command = "python3 -m ReMatch " + args['video_id_day_one'] + " " + args['video_type_day_one'] + " " + args['event_key'] + " " + args['event_type'] + " " + args['video_id_day_two'] + " " + args['video_type_day_two'] + " " + args['video_id_day_three'] + " " + args['video_type_day_three']
    subprocess.Popen(command, shell=True)
    return send_from_directory('.', 'Execute.html')

if __name__ == "__main__":
    app.run()
