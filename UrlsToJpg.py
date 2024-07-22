import os
import requests

folder_path = r'F:\Tinder Storage\Predicting'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


with open('urls.txt', 'r') as file:
    lines = file.readlines()


counter = 1

for line in lines:
    if line.startswith('https://'):
        
        url = line.strip()

        response = requests.get(url)
        
        if response.status_code == 200:
            file_name = f'image_{counter}.jpg'
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'wb') as img_file:
                img_file.write(response.content)
                
            print(f'Saved {file_name}')
            counter += 1
        else:
            print(f'Failed to fetch {url}')
