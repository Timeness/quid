const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('room') || urlParams.get('roomPlay');
const ws = new WebSocket(`wss://${location.host.replace('http', '')}/ws/${roomId}`);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.action === "play") {
        document.getElementById('player').src = '/' + data.file_path;
        document.getElementById('player').play();
        document.getElementById('info').innerText = `Now Playing: ${data.title}`;
    }
};

async function playSong() {
    const query = document.getElementById('query').value;
    await fetch(`/play_song/${roomId}?query=${encodeURIComponent(query)}`, { method: 'POST' });
}
