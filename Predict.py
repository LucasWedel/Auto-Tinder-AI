import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
from tensorflow.keras.applications.vgg16 import preprocess_input

def load_images_from_folder(folder):
    """Load images from a directory and preprocess them."""
    images = []
    image_names = []
    for filename in os.listdir(folder):
        if filename.endswith('.jpg'):
            img_path = os.path.join(folder, filename)
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            images.append(img_array)
            image_names.append(filename)
    if images:
        return np.vstack(images), image_names
    else:
        return np.array([]), image_names

def predict_images(model_path, images_folder):
    """Load a model and predict the class of each image in a folder, and calculate the average for each prefix."""
    model = load_model(model_path)
    images, image_names = load_images_from_folder(images_folder)
    if images.size == 0:
        print("No images found in the folder.")
        return []

    predictions = model.predict(images)
    print("Raw predictions:", predictions)  # Print the raw predictions

    prefix_sums = {'0_': 0.0, '1_': 0.0}
    prefix_counts = {'0_': 0, '1_': 0}

    for i, prediction in enumerate(predictions):
        prefix = image_names[i][:2]  # Extract prefix (e.g., '0_' or '1_')
        if prefix in prefix_sums:
            prefix_sums[prefix] += prediction[0]  # Assuming binary classification and prediction is a list with one element
            prefix_counts[prefix] += 1

    # Calculate averages
    prefix_averages = {prefix: (prefix_sums[prefix] / prefix_counts[prefix] if prefix_counts[prefix] > 0 else 0) for prefix in prefix_sums}

   
        
    results = {}
    for i, prediction in enumerate(predictions):
        results[image_names[i]] = 'Attractive' if prediction >= 0.238 else 'Not Attractive'
        
    # Print averages
    for prefix, avg in prefix_averages.items():
        print(f'Average for {prefix}: {avg}')
    return results

# Example usage
model_path = r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\saved_model_h5.h5'
images_folder = r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\New_Images'

if __name__ == "__main__":
    results = predict_images(model_path, images_folder)
    for image_name, result in results.items():
        print(f'{image_name}: {result}')
