from flask import Flask, request, jsonify
import subprocess
import threading
import time
import requests
from werkzeug.utils import secure_filename
import os
import tempfile
import image_processor  
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

RASA_COMMAND = "cd ./rasa && rasa run --port 5005"

rasa_process = None

def start_rasa():
    global rasa_process
    try:
        print("Starting Rasa...")
        rasa_process = subprocess.Popen(
            RASA_COMMAND,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  
        )
        
        for line in iter(rasa_process.stdout.readline, ''):
            print(f"Rasa stdout: {line.strip()}")
        for line in iter(rasa_process.stderr.readline, ''):
            print(f"Rasa stderr: {line.strip()}")
        
        print("Rasa started successfully.")
        
    except Exception as e:
        print(f"Failed to start Rasa: {e}")

def run_rasa():
    time.sleep(5)  
    start_rasa()

rasa_thread = threading.Thread(target=run_rasa)
rasa_thread.start()

@app.route('/message', methods=['POST'])
def message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Send user message to Rasa
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    try:
        response = requests.post(rasa_url, json={'message': user_message})
        response.raise_for_status()  # Ensure we raise an exception for HTTP errors
        rasa_response = response.json()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    # Return Rasa's response to the client
    return jsonify(rasa_response)

@app.route('/test', methods=['GET'])
def test_rasa():
    # Define a test message
    test_message = {'message': 'Hello, Rasa!'}
    
    # Send the test message to Rasa
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    try:
        response = requests.post(rasa_url, json=test_message)
        response.raise_for_status()  # Ensure we raise an exception for HTTP errors
        rasa_response = response.json()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    # Return Rasa's response to the client
    return jsonify({'test_response': rasa_response})

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Use tempfile to create a temporary directory and file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        file_path = temp_file.name
        file.save(file_path)
    
    # Process the image
    try:
        result = image_processor.process_image(file_path)
    except Exception as e:
        result = {'error': str(e)}
    
    # Optionally delete the file after processing
    os.remove(file_path)
    
    return jsonify(result), 200  # Return JSON response with appropriate content type

@app.route('/shutdown', methods=['POST'])
def shutdown():
    global rasa_process
    if rasa_process:
        rasa_process.terminate()
        rasa_process.wait()
        print("Rasa process terminated.")
    return jsonify({'status': 'Rasa stopped'}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Enable debug mode for more detailed error output
