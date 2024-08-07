import sys
import json
from PIL import Image
import easyocr

def process_image(image_path):
    try:
        # Initialize EasyOCR Reader
        reader = easyocr.Reader(['ar'])  # Use the language you need

        # Open the image file
        img = Image.open(image_path)

        # Use EasyOCR to do OCR on the image
        result = reader.readtext(image_path)

        # Extract and join text from OCR result
        text = ' '.join([res[1] for res in result])
        
        # Create a JSON response
        response = {'text': text.strip()}
        return json.dumps(response)
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Invalid arguments'}), file=sys.stderr)
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = process_image(image_path)
    print(result)
