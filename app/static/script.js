document.getElementById('startButton').onclick = function() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(stream => {
            const audioContext = new AudioContext();
            const source = audioContext.createMediaStreamSource(stream);
            const processor = audioContext.createScriptProcessor(1024, 1, 1);

            source.connect(processor);
            processor.connect(audioContext.destination);

            const socket = new WebSocket('ws://localhost:8036/ws');
            socket.binaryType = 'arraybuffer';

            processor.onaudioprocess = function(e) {
                if (socket.readyState === WebSocket.OPEN) {
                    socket.send(e.inputBuffer.getChannelData(0));
                }
            };
        })
        .catch(error => {
            console.error('Error accessing the microphone', error);
        });
};
