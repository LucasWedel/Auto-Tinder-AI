import os

# Replace Path
image_dir = r'C:\Users'

files = os.listdir(image_dir)

for filename in files:
    if filename.endswith('.jpg') and (filename.startswith('0_') or filename.startswith('1_')):
        new_name = filename[2:]
        os.rename(os.path.join(image_dir, filename), os.path.join(image_dir, new_name))
