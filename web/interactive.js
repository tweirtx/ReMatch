function addDay() {
    const days = document.getElementById('days');
    const number = days.children.length + 1;
    const html =
    `<div class="col-md-4 mb-3">
        <div class="card p-3">
            <h5 class="card-title">Day ${number}</h5>
            <label for="video_id">Video ID</label>
            <input class="form-control mb-3" id="video_id_${number}" name="days[][video_id]" type="text" required>
            <label for="video_type_day_one">Video Type</label>
            <select class="custom-select" id="video_type_${number}">
                <option value="twitch" class="notranslate">Twitch</option>
            </select>
        </div>
    </div>`;
    days.innerHTML += html;
}

document.addEventListener('DOMContentLoaded', addDay);

function execute() {
    let videos = [];
    const videoElements = document.getElementsByClassName("card p-3");
    if(videoElements.length !== 1) {
        for (let num of range(1, videoElements.length)) {
            videos += JSON.stringify({video_id: getVal('video_id_' + num), video_type: getVal('video_type_' + num)});
        }
    }
    else if (videoElements.length === 1) {
        videos += JSON.stringify({video_id: getVal('video_id_1'), video_type: getVal('video_type_1')});
    }
    let data = {
        event_key: getVal('event_key'),
        event_type: getVal('event_type'),
        videos: "[" + videos.toString().replace('}{', '},{') + "]"
    };
    console.log(JSON.stringify(data));
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'execute_json', true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(data));
}

function getVal(key) {
    return document.getElementById(key).value;
}

function* range(start, end) { //Because JavaScript can't do a basic function apparently
    yield start;
    if (start === end) return;
    yield* range(start + 1, end);
}
