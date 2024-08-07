import sys
import json
from PIL import Image
import pytesseract

def process_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        
        # Create a JSON response
        result = {'text': text.strip()}
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Invalid arguments'}), file=sys.stderr)
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = process_image(image_path)
    print(result)
