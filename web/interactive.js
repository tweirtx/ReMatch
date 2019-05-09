function addDay() {
    const days = document.getElementById('days');
    const number = days.children.length + 1;
    const html =
    `<div class="col-md-4 mb-3">
        <div class="card p-3">
            <h5 class="card-title">Day ${number}${number > 1 ? ' (optional)' : ''}</h5>
            <label for="video_id">Video ID</label>
            <input class="form-control mb-3" id="video_id" name="days[][video_id]" type="text" required>

            <label for="video_type_day_one">Video Type</label>
            <select class="custom-select" id="video_type" name="days[][type]">
                <option value="twitch" class="notranslate">Twitch</option>
                <option value="youtube" class="notranslate">YouTube</option>
            </select>
        </div>
    </div>`;
    days.innerHTML += html;
}

document.addEventListener('DOMContentLoaded', addDay);

function execute() {
    
}