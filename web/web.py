import subprocess
import json
from flask import request, Flask, send_from_directory

app = Flask("ReMatch-Web")


@app.route('/')
def front_page():
    return send_from_directory('web', "index.html")


@app.route('/interactive.js')
def js():
    return send_from_directory('web', "interactive.js")


@app.route('/execute', methods=['POST', 'GET'])
def execute():
    return send_from_directory('web', "execute.html")


@app.route('/bootstrap.css')
def css():
    return send_from_directory('web', "bootstrap.css")


@app.route('/nginx.html')
def nginx():
    return send_from_directory('web', "nginx.html")


@app.route('/darkly.min.css')
def darklycss():
    return send_from_directory('web', "darkly.min.css")


@app.route('/execute_json', methods=['POST'])
def parse_json():
    vals = json.dumps(request.json)
    print(vals)
    with open('process_me_next.json', 'w') as f:
        f.write(vals)
    command = "python3 -m ReMatch"
    subprocess.Popen(command, shell=True)
    return ""


@app.route('/set_tba_key', methods=['POST'])
def set_tba_key():
    with open('tbakey.txt', 'w') as f:
        f.write(request.args.get("key"))
    return "Key set successfully!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
