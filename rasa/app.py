from flask import Flask, request, jsonify, send_file
from image_processor import process_image
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        image_bytes = file.read()
        processed_image_bytes = process_image(image_bytes)

        # Convert bytes to a stream for sending as a response
        processed_image_stream = io.BytesIO(processed_image_bytes)
        
        return send_file(processed_image_stream, mimetype='image/png', as_attachment=True, download_name='processed_image.png')

    return jsonify({'error': 'Unsupported file type'}), 400

if __name__ == '__main__':
    app.run(port=5000)
