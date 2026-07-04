from resvg_py import svg_to_bytes
import cv2
import numpy
from PIL import Image
import sys
import requests
import os
import zipfile
import shutil
from io import BytesIO

# Här får vi våra svg emojis ifrån
TWEMOJI_URL = "https://github.com/twitter/twemoji/archive/refs/tags/v14.0.2.zip"
TWEMOJI_SVGS_PATH = 'twemoji-14.0.2/assets/svg/'

EMOJI_PATH_SVG = 'Backend/Assets/Emojis_SVG'
EMOJI_PATH_PNG = 'Backend/Assets/Emojis_PNG'

EMOJI_SIZE = 16

# Från https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def download_emojis():
    with open('emojis.zip', "wb") as f:
        print("Downloading %s" % 'emojis.zip')
        response = requests.get(TWEMOJI_URL, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
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
    print(f'Extracting emojis.zip to {EMOJI_PATH_SVG}')

    if not os.path.exists(EMOJI_PATH_SVG):
        os.makedirs(EMOJI_PATH_SVG)

    z = zipfile.ZipFile('emojis.zip')

    for file in z.namelist():
        if file.startswith(TWEMOJI_SVGS_PATH) and file != TWEMOJI_SVGS_PATH:
            filename = os.path.basename(file)
            if filename:
                target_path = os.path.join(EMOJI_PATH_SVG, filename)
                with z.open(file) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)

def convert_svgs_to_pngs():
    if not os.path.exists:
        os.makedirs(EMOJI_PATH_PNG)

    for i, filename in enumerate(os.listdir(EMOJI_PATH_SVG)):
        if filename.endswith('.svg'):
            svg_path = os.path.join(EMOJI_PATH_SVG, filename)
            png_path = os.path.join(EMOJI_PATH_PNG, filename.replace('.svg', '.png'))

            png_bytes = svg_to_bytes(svg_path=svg_path, width=EMOJI_SIZE, height=EMOJI_SIZE)
            rendered_img = Image.open(BytesIO(bytes(png_bytes))).convert('RGBA')

            canvas = Image.new('RGBA', (EMOJI_SIZE, EMOJI_SIZE), (0, 0, 0, 0))
            paste_x = (EMOJI_SIZE - rendered_img.width) // 2
            paste_y = (EMOJI_SIZE - rendered_img.height) // 2
            canvas.paste(rendered_img, (paste_x, paste_y), rendered_img)
            canvas.save(png_path)

            print(f'({i+1}/{len(os.listdir(EMOJI_PATH_SVG))}) | {filename} converted to PNG')

if os.path.isfile('emojis.zip'):
    print("emojis.zip already exists")
else:
    print("emojis.zip does not exist")
    download_emojis()

if not os.path.exists(EMOJI_PATH_SVG):
    os.makedirs(EMOJI_PATH_SVG)

if len(os.listdir(EMOJI_PATH_SVG)) == 0:
    extract_emojis()

else:
    print('emojis.zip already extracted')

if not os.path.exists(EMOJI_PATH_PNG):
    os.makedirs(EMOJI_PATH_PNG)

if len(os.listdir(EMOJI_PATH_PNG)) == 0:
    convert_svgs_to_pngs()