function addDay() {
    var days = document.getElementById('days');
    var number = days.children.length + 1;
    var html =
    `<div class="col-md-4 mb-3">
        <div class="card p-3" day data-number="${number}">
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
    console.log("Executing...");
    var data = {
        event_key: getVal('event_key'),
        event_type: getVal('event_type'),
        email: getVal('email'),
        videos: Array.from(document.querySelectorAll('[day]')).map(function (day) {
            var number = day.dataset.number;
            return {video_id: getVal('video_id_' + number), video_type: getVal('video_type_' + number)};
        })
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
