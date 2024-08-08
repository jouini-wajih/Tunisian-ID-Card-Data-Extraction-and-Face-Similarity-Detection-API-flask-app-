import os
from pathlib import Path
from PIL import Image
import face_recognition
from object_extractor import Extractor, FRONTALFACE_ALT2

def extract_faces_from_image(image_path, output_directory, output_prefix="face_", start_count=1):
    """Extract faces from a single image and save them to the output directory with the same name as the original image."""
    try:
        # Ensure output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Create a temporary directory to store extracted faces
        temp_directory = Path(output_directory) / "temp_faces"
        if not temp_directory.exists():
            temp_directory.mkdir(parents=True)

        # Extract faces from the single image
        Extractor.extract(
            image_path,
            cascade_file=FRONTALFACE_ALT2,
            output_directory=str(temp_directory),
            output_prefix=output_prefix,
            start_count=start_count
        )

        # Rename and move the extracted face files to the output directory
        for file in temp_directory.iterdir():
            if file.is_file():
                # Construct the new file name based on the original image name
                new_file_name = f"{Path(image_path).stem}_{file.name}"
                new_file_path = Path(output_directory) / new_file_name
                file.rename(new_file_path)

        # Remove the temporary directory if empty
        temp_directory.rmdir()

        print(f"Faces extracted from {image_path} and saved to {output_directory}")

    except Exception as e:
        print(f"Error extracting faces from {image_path}: {e}")

def process_images_in_directory(input_directory, output_directory, output_prefix="face_"):
    """Process all images in the input directory and save results to the output directory."""
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the input directory
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)

        # Check if the file is an image (basic check for .jpg and .png extensions)
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Processing {file_path}...")

            # Define output directory for each image (optional, or use a common output directory)
            image_output_directory = output_directory
            if not os.path.exists(image_output_directory):
                os.makedirs(image_output_directory)

            # Extract faces from the image
            extract_faces_from_image(file_path, image_output_directory, output_prefix)

# Define paths
input_directory = './cards'  # Replace with your input directory
output_directory = 'output'  # Replace with your output directory

# Call the function to process all images
#process_images_in_directory(input_directory, output_directory)


def find_best_matching_face(known_image_path, people_directory, output_directory):
    """Find the best matching face from a directory of face images."""
    try:
        # Load the known image
        known_image = face_recognition.load_image_file(known_image_path)

        # Encode the known image
        known_image_encodings = face_recognition.face_encodings(known_image)
        if not known_image_encodings:
            print("No faces found in the known image.")
            return

        known_image_encoding = known_image_encodings[0]

        # Variables to keep track of the most similar face match we've found
        best_face_distance = 1.0
        best_face_image = None
        best_face_path = None

        # Loop through each file in the people directory
        for image_path in Path(people_directory).iterdir():
            # Skip non-image files
            if not image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                continue

            # Load the image to check
            unknown_image = face_recognition.load_image_file(image_path)

            # Get the face encodings for the current image
            face_encodings = face_recognition.face_encodings(unknown_image)

            if not face_encodings:
                print(f"No faces found in {image_path}. Skipping.")
                continue  # Skip images with no faces

            # Check each face encoding in the current image
            for face_encoding in face_encodings:
                face_distance = face_recognition.face_distance([face_encoding], known_image_encoding)[0]

                print(f"Comparing {image_path} with distance {face_distance}")

                # If this face is more similar to our known image than we've seen so far, save it
                if face_distance < best_face_distance:
                    best_face_distance = face_distance
                    best_face_image = unknown_image
                    best_face_path = image_path

        if best_face_image is not None:
            # Convert the image to PIL format
            pil_image = Image.fromarray(best_face_image)

            # Save the best face image to the output directory
            if not Path(output_directory).exists():
                Path(output_directory).mkdir(parents=True)

            output_path = Path(output_directory) / Path(known_image_path).name
            pil_image.save(output_path)

            print(f"Best matching face saved to {output_path}")
        else:
            print("No matching faces found.")

    except Exception as e:
        print(f"Error finding best matching face: {e}")

# Example usage:



def extract_face_from_image(image_path, output_directory='./output2', output_prefix="face_", start_count=1):
    """Extract faces from a single image and save them to the output directory with the same name as the original image."""
    try:
        # Ensure output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Create a temporary directory to store extracted faces
        temp_directory = Path(output_directory) / "temp_faces"
        if not temp_directory.exists():
            temp_directory.mkdir(parents=True)

        # Extract faces from the single image
        Extractor.extract(
            image_path,
            cascade_file=FRONTALFACE_ALT2,
            output_directory=str(temp_directory),
            output_prefix=output_prefix,
            start_count=start_count
        )

        # Move the extracted face files to the output directory
        face_paths = []
        for file in temp_directory.iterdir():
            if file.is_file():
                # Construct the new file name based on the original image name
                new_file_name = f"{Path(image_path).stem}_{file.name}"
                new_file_path = Path(output_directory) / new_file_name
                file.rename(new_file_path)
                face_paths.append(new_file_path)

        # Remove the temporary directory if empty
        temp_directory.rmdir()

        print(f"Faces extracted from {image_path} and saved to {output_directory}")

        if face_paths:
            return face_paths[0]  # Return the path of the first (or only) face image
        else:
            return None

    except Exception as e:
        print(f"Error extracting faces from {image_path}: {e}")
        return None

def get_best_similarity_distance(known_image_path, people_directory='./output'):
    """Find the best matching face from a directory of face images and return the best similarity distance."""
    try:
        # Load the known image
        known_image = face_recognition.load_image_file(known_image_path)

        # Encode the known image
        known_image_encodings = face_recognition.face_encodings(known_image)
        if not known_image_encodings:
            print("No faces found in the known image.")
            return None

        known_image_encoding = known_image_encodings[0]

        # Variables to keep track of the most similar face match we've found
        best_face_distance = 1.0

        # Loop through each file in the people directory
        for image_path in Path(people_directory).iterdir():
            # Skip non-image files
            if not image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                continue

            # Load the image to check
            unknown_image = face_recognition.load_image_file(image_path)

            # Get the face encodings for the current image
            face_encodings = face_recognition.face_encodings(unknown_image)

            if not face_encodings:
                print(f"No faces found in {image_path}. Skipping.")
                continue  # Skip images with no faces

            # Check each face encoding in the current image
            for face_encoding in face_encodings:
                face_distance = face_recognition.face_distance([face_encoding], known_image_encoding)[0]

                print(f"Comparing {image_path} with distance {face_distance}")

                # If this face is more similar to our known image than we've seen so far, save it
                if face_distance < best_face_distance:
                    best_face_distance = face_distance

        if best_face_distance < 1.0:  # If a valid face was found
            print(f"Best matching face distance: {best_face_distance}")
            return best_face_distance
        else:
            print("No matching faces found.")
            return None

    except Exception as e:
        print(f"Error finding best matching face: {e}")
        return None

# Example usage:
# Extract a face from an image and get the path
extracted_face_path = extract_face_from_image('./known_image.jpg')
print(f"Extracted face path: {extracted_face_path}")

# Find the best similarity distance
if extracted_face_path:
    best_distance = get_best_similarity_distance(extracted_face_path, './output')
    print(f"Best similarity distance: {best_distance}")


