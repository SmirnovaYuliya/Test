from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            start_time = time.time()
            file.save(file_path)
            end_time = time.time()

            duration = end_time - start_time

            return jsonify({
                'filename': filename,
                'duration': duration,
                'download_url': f'/download/{filename}'
            })

        return jsonify({'error': 'No file provided'}), 400

    return jsonify({'error': 'Invalid request'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000, debug=True)
