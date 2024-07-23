import os
import requests
import random
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Edit your folder path
folder_path = r'F:\Tinder Storage\Predicting'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
model_path = r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\saved_model_h5.h5'
images_folder = r'F:\Tinder Storage\Predicting'
old_urls_file = 'old_urls.txt'

def space_search_and_scrape(driver):
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.SPACE)
    time.sleep(random.uniform(4, 4))  
    
    elements = driver.find_elements(By.CSS_SELECTOR, '[style*="background-image"][style*="gotinder.com/u/"]')
    scraped_urls = []
    for element in elements:
        style_attribute = element.get_attribute("style")
        url_start_index = style_attribute.find('url("') + len('url("')
        url_end_index = style_attribute.find('")', url_start_index)
        
        if url_start_index != -1 and url_end_index != -1:
            url = style_attribute[url_start_index:url_end_index]
            scraped_urls.append(url)
        else:
            print("URL not found for element:", element.get_attribute("outerHTML"))
            
    return scraped_urls

def load_images_from_folder(folder):
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
    model = load_model(model_path)
    images, image_names = load_images_from_folder(images_folder)
    if images.size == 0:
        print("No images found in the folder.")
        return []

    predictions = model.predict(images)
    print("Raw predictions:", predictions)  
    total_sum = 0
    total_count = 0

    for prediction in predictions:
        total_sum += prediction[0]  
        total_count += 1

    average_prediction = total_sum / total_count if total_count > 0 else 0.0
    print(f'Average prediction: {average_prediction}')
    results = {}
    for i, prediction in enumerate(predictions):
        results[image_names[i]] = 'Attractive' if prediction[0] >= 0.238 else 'Not Attractive'
        
    time.sleep(random.uniform(2, 2))  
    
    if average_prediction > 0.225:
        print('The person is attractive')
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_RIGHT)
    else:
        print('The person is not attractive')
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ARROW_LEFT)

    return results

# Put your chromedriver path
PATH = r"C:\Users\lucas\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
opts = webdriver.ChromeOptions()
opts.add_argument("--user-data-dir=C:\\Users\\lucas\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=opts)
driver.get("https://tinder.com/app/recs")
print('Sleeping for 30 seconds first time launching')
time.sleep(random.uniform(30, 35))

if os.path.exists(old_urls_file):
    with open(old_urls_file, 'r') as file:
        old_urls = set(line.strip() for line in file)
else:
    old_urls = set()

while True:
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.bullet[aria-label*="1 af"][aria-label*="tilgængelige billeder"]')
    
    total_images = 0

    if buttons and len(buttons) > 1:
        button = buttons[1]
        aria_label = button.get_attribute("aria-label")
        attempt_count = 0
        max_attempts = 10
        
        while attempt_count < max_attempts:
            if aria_label:
                parts = aria_label.split(" ")
                if "af" in parts and "tilgængelige" in parts:
                    x_index = parts.index("tilgængelige") - 1
                    if x_index >= 0:
                        total_images = parts[x_index]
                        print("Total available images:", total_images)
                        try:
                            total_images = int(total_images)
                            break  
                        except ValueError:
                            print(f"Error converting total_images to int: {total_images}")
                    else:
                        print("Could not determine the total number of available images.")
                else:
                    print("Could not find the relevant parts in the aria-label attribute.")
            else:
                print("aria-label attribute not found for the button.")
            
            attempt_count += 1
            if total_images is None or total_images == 0:
                print(f"Attempt {attempt_count} failed to find total_images. Retrying...")
                time.sleep(random.uniform(1, 2))
        
    total_images = int(total_images)
    
    unique_urls = set()
    unique_base_urls = set()
    unique_original_urls = set()

    for i in range(total_images):
        scraped_urls = space_search_and_scrape(driver)
        base_urls = [url.split('?')[0] for url in scraped_urls[1:]]
        unique_base_urls.update(base_urls)
        unique_original_urls.update(scraped_urls[1:])

    new_unique_original_urls = unique_original_urls - old_urls
    
    urltojpgimagecounter = 1
    for url in new_unique_original_urls:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f'image_{urltojpgimagecounter}.jpg'
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as img_file:
                img_file.write(response.content)
            urltojpgimagecounter += 1
        else:
            print(f'Failed to fetch {url}')

    elements = driver.find_elements(By.TAG_NAME, 'div')
    elements = driver.find_elements(By.CSS_SELECTOR, '[style*="background-image"][style*="gotinder.com/u/"]')
    separator = "\n----------------\n"

    print("Unique URLs:", separator.join(unique_urls))

    with open('urls.txt', 'r') as f:
        existing_base_urls = set(line.split('?')[0].strip() for line in f)
    unique_base_urls -= existing_base_urls
    new_urls = [url for url in new_unique_original_urls if url.split('?')[0] in unique_base_urls]
    
    predict_images(model_path, images_folder)

    if new_urls:
        url_string = separator.join(new_urls)
        url_string += "\n----------------\n"
        with open('urls.txt', 'a') as f:
            f.write(url_string)

    old_urls.update(unique_original_urls)
    with open(old_urls_file, 'w') as file:
        file.write("\n".join(old_urls))

    folder_path = r'F:\Tinder Storage\Predicting'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')        

    print('Resetting model - Cooldown 5 Seconds')       
    print('---------')
    time.sleep(random.uniform(5, 5))
