from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
detector = None

@app.route('/')
def index():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Detector</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>Emotion Detector</h1>
    <div class="container">
        <video id="video" autoplay></video>
        <div id="results"></div>
    </div>
    <button id="capture">Capture Emotion</button>
    <p>Press 's' to take screenshot, 'q' to quit detection.</p>
    <script>
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture');
        const resultsDiv = document.getElementById('results');

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
            })
            .catch(err => {
                console.error('Error accessing webcam:', err);
                resultsDiv.innerHTML = '<p>Error: Could not access webcam.</p>';
            });

        captureBtn.addEventListener('click', () => {
            if (video.videoWidth === 0) {
                resultsDiv.innerHTML = '<p>Video not ready. Please wait for the camera to load.</p>';
                return;
            }
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            const imageData = canvas.toDataURL('image/jpeg').split(',')[1];

            fetch('/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    resultsDiv.innerHTML = `
                        <p><strong>Dominant Emotion:</strong> ${data.dominant_emotion} (${(data.confidence * 100).toFixed(2)}%)</p>
                        <ul>
                            ${Object.entries(data.all_emotions).map(([emotion, prob]) => `<li>${emotion}: ${(prob * 100).toFixed(2)}%</li>`).join('')}
                        </ul>
                    `;
                }
            })
            .catch(err => {
                console.error('Error:', err);
                resultsDiv.innerHTML = '<p>Error detecting emotion.</p>';
            });
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'q' || e.key === 'Q') {
                if (video.srcObject) {
                    video.srcObject.getTracks().forEach(track => track.stop());
                }
                document.body.innerHTML = '<h1>Page Closed</h1>';
            }
            if (e.key === 's' || e.key === 'S') {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0);
                const link = document.createElement('a');
                link.download = 'emotion_screenshot.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            }
        });
    </script>
</body>
</html>"""
    return html

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/detect', methods=['POST'])
def detect():
    global detector
    if detector is None:
        from scripts.emotion_detector import EmotionDetector
        detector = EmotionDetector()
    data = request.get_json()
    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'No image data'})
    result = detector.detect_emotion_from_image(image_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
