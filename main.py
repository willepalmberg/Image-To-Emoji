import cv2
import numpy
from PIL import Image
import emoji
import sys
import requests
import os
import zipfile
import shutil

# Här får vi våra svg emojis ifrån
TWEMOJI_URL = "https://github.com/twitter/twemoji/archive/refs/tags/v14.0.2.zip"


# Från https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def download_emojis():
    with open('emojis.zip', "wb") as f:
        print("Downloading %s" % 'emojis.zip')
        response = requests.get(TWEMOJI_URL, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

def extract_emojis():
    print(f'Extracting emojis.zip to {emoji_path}')

    if not os.path.exists(emoji_path):
        os.makedirs(emoji_path)

    z = zipfile.ZipFile('emojis.zip')
    prefix = 'twemoji-14.0.2/assets/svg/'

    for file in z.namelist():
        if file.startswith(prefix) and file != prefix:
            filename = os.path.basename(file)
            if filename:
                target_path = os.path.join(emoji_path, filename)
                with z.open(file) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)

start_data = cv2.imread('test_image.jpg')
start_img = Image.fromarray(start_data)

if os.path.isfile('emojis.zip'):
    print("emojis.zip already exists")
else:
    print("emojis.zip does not exist")
    download_emojis()

emoji_path = 'Backend/Assets/Emojis_SVG'
if len(os.listdir(emoji_path)) == 0:
    extract_emojis()

else:
    print('emojis.zip already extracted')
