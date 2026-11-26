const audio = document.getElementById('audio');
const playBtn = document.getElementById('playPause');
const seek = document.getElementById('seek');

let queue = [];
let current = 0;

function fmt(seconds) {
    if (!Number.isFinite(seconds)) {
        return '0:00';
    }

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = String(Math.floor(seconds % 60)).padStart(2, '0');

    return `${minutes}:${remainingSeconds}`;
}

function loadTrack(button, autoplay = true) {
    const src = button.dataset.audio;

    if (!src) {
        return;
    }

    audio.src = src;
    document.getElementById('nowTitle').textContent = button.dataset.title || 'Unknown track';
    document.getElementById('nowArtist').textContent = button.dataset.artist || '';

    const cover = button.dataset.cover;
    const miniCover = document.getElementById('miniCover');

    miniCover.textContent = cover ? '' : '♫';
    miniCover.style.backgroundImage = cover ? `url('${cover}')` : '';

    queue = [...document.querySelectorAll('[data-audio]')];
    current = Math.max(0, queue.indexOf(button));

    if (autoplay) {
        audio.play().catch(() => {});
    }
}

document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-audio]');

    if (button) {
        loadTrack(button);
    }
});

playBtn.addEventListener('click', () => {
    if (!audio.src) {
        const firstTrack = document.querySelector('[data-audio]');

        if (firstTrack) {
            loadTrack(firstTrack);
        }

        return;
    }

    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
});

audio.addEventListener('play', () => {
    playBtn.textContent = 'Ⅱ';
});

audio.addEventListener('pause', () => {
    playBtn.textContent = '▶';
});

audio.addEventListener('timeupdate', () => {
    seek.value = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
    document.getElementById('currentTime').textContent = fmt(audio.currentTime);
    document.getElementById('duration').textContent = fmt(audio.duration);
});

seek.addEventListener('input', () => {
    if (audio.duration) {
        audio.currentTime = (seek.value / 100) * audio.duration;
    }
});

document.getElementById('volume').addEventListener('input', (event) => {
    audio.volume = event.target.value;
});

function step(direction) {
    if (!queue.length) {
        queue = [...document.querySelectorAll('[data-audio]')];
    }

    if (!queue.length) {
        return;
    }

    current = (current + direction + queue.length) % queue.length;
    loadTrack(queue[current]);
}

document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);
audio.addEventListener('ended', () => step(1));
audio.volume = 0.8;
