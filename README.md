# Tunisian ID Card Data Extraction and Face Similarity Detection API

## Description

This project provides an API built with Flask that integrates several functionalities:

1. **Chatbot Integration**: Connects with Rasa to handle conversational queries.
2. **Face Detection and Similarity**: Extracts faces from images and compares them for similarity.
3. **Tunisian ID Card Data Extraction**: Extracts and processes Arabic text from Tunisian ID cards, including extracting birthdates, ID numbers, and places.

## Features

- **Rasa Chatbot**: Integrates a Rasa chatbot for handling messages.
- **Image Processing**: 
  - Detects and extracts faces from images.
  - Compares faces for similarity.
  - Preprocesses images for text extraction.
- **Text Extraction**:
  - Detects Arabic text from images.
  - Extracts relevant information such as birthdates and ID numbers.
  - Corrects and translates Arabic text.
- **Face Similarity Detection**: Finds the best matching face from a directory of known faces.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Rasa
- `face_recognition` library
- `easyocr` library
- `Pillow` library
- `opencv-python` library
- Other dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/tunisian-id-card-api.git
    cd tunisian-id-card-api
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Rasa and its dependencies:

    ```bash
    pip install rasa
    ```

5. Download and set up Rasa models and configurations as needed.

### Usage

1. Start the Flask API:

    ```bash
    python app.py
    ```

2. In a separate terminal, start the Rasa server:

    ```bash
    cd rasa
    rasa run --port 5005
    ```

3. Use `curl` or any API client to interact with the API endpoints:

    - **Send a message to the Rasa chatbot:**

        ```bash
        curl -X POST http://localhost:5000/message -H "Content-Type: application/json" -d '{"message": "Hello"}'
        ```

    - **Test Rasa:**

        ```bash
        curl -X GET http://localhost:5000/test
        ```

    - **Process an image:**

        ```bash
        curl -X POST http://localhost:5000/process-image -F "file=@/path/to/your/image.jpg"
        ```

    - **Shutdown Rasa:**

        ```bash
        curl -X POST http://localhost:5000/shutdown
        ```

### Code Explanation

- **`app.py`**: Main Flask application that provides endpoints for message handling, image processing, and Rasa management.
- **`image_processor.py`**: Contains functions for face extraction, similarity detection, text detection, and Arabic text processing.

### Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues or have suggestions, please open an issue on GitHub.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- **Rasa**: For conversational AI capabilities.
- **face_recognition**: For face detection and similarity comparison.
- **easyocr**: For optical character recognition (OCR) of Arabic text.

---

**Note**: Ensure you have all the necessary models and data files required for Rasa and face recognition functionalities.
