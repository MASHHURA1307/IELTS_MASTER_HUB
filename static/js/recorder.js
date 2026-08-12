// Web Audio MediaRecorder logic for Speaking section

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startRecBtn');
    const stopBtn = document.getElementById('stopRecBtn');
    const recTimer = document.getElementById('recTimer');
    const recStatus = document.getElementById('recStatus');
    const audioPreviewContainer = document.getElementById('audioPreviewContainer');
    const audioPlayback = document.getElementById('audioPlayback');
    const audioFileInput = document.getElementById('audioFileInput');

    let mediaRecorder = null;
    let audioChunks = [];
    let recInterval = null;
    let secondsElapsed = 0;

    if (startBtn && stopBtn) {
        startBtn.addEventListener('click', async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayback.src = audioUrl;
                    audioPreviewContainer.classList.remove('d-none');

                    // Create file for input
                    const file = new File([audioBlob], `speaking_${Date.now()}.webm`, { type: 'audio/webm' });
                    const container = new DataTransfer();
                    container.items.add(file);
                    audioFileInput.files = container.files;
                };

                mediaRecorder.start();
                secondsElapsed = 0;
                recStatus.textContent = "Ovoz yozilmoqda... Qayta bosib to'xtating.";
                recStatus.classList.add('text-danger', 'fw-bold');

                startBtn.classList.add('d-none');
                stopBtn.classList.remove('d-none');

                recInterval = setInterval(() => {
                    secondsElapsed++;
                    const m = Math.floor(secondsElapsed / 60);
                    const s = secondsElapsed % 60;
                    recTimer.textContent = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
                }, 1000);

            } catch (err) {
                alert("Mikrofonga kirishga ruxsat berilmadi yoki brauzeringiz qo'llab-quvvatlamaydi!");
                console.error("Mic access error:", err);
            }
        });

        stopBtn.addEventListener('click', () => {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                clearInterval(recInterval);

                recStatus.textContent = "Yozib olish yakunlandi! Quyida tinglab ko'rishingiz mumkin.";
                recStatus.classList.remove('text-danger');
                recStatus.classList.add('text-success');

                stopBtn.classList.add('d-none');
                startBtn.classList.remove('d-none');
            }
        });
    }
});
