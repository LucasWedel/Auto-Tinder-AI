import os

#Insert path
directory_path = r'F:'

start_number = 914

files = os.listdir(directory_path)

files.sort()

for file in files:
    new_filename = f"image_{start_number}.jpg"
    
    old_file_path = os.path.join(directory_path, file)
    new_file_path = os.path.join(directory_path, new_filename)
    
    os.rename(old_file_path, new_file_path)
    
    start_number += 1

print("Renaming complete.")