from io import BytesIO

import cv2
import numpy
from PIL import Image
import emoji
import sys
import requests
import os
import zipfile
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
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

    for filename in os.listdir(EMOJI_PATH_SVG):
        if filename.endswith('.svg'):
            svg_path = os.path.join(EMOJI_PATH_SVG, filename)
            png_path = os.path.join(EMOJI_PATH_PNG, filename.replace('.svg', '.png'))

            drawing = svg2rlg(svg_path)

            scale = min(EMOJI_SIZE / drawing.width, EMOJI_SIZE / drawing.height)
            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)

            buffer = BytesIO()
            renderPM.drawToFile(drawing, buffer, fmt="PNG", bg=0x000000)

            buffer.seek(0)
            rendered_emoji = Image.open(buffer)

            canvas = Image.new('RGBA', (EMOJI_SIZE, EMOJI_SIZE), (0, 0, 0, 0))
            paste_x = (EMOJI_SIZE - rendered_emoji.width) // 2
            paste_y = (EMOJI_SIZE - rendered_emoji.height) // 2
            canvas.paste(rendered_emoji, (paste_x, paste_y))

            canvas.save(png_path)

if os.path.isfile('emojis.zip'):
    print("emojis.zip already exists")
else:
    print("emojis.zip does not exist")
    download_emojis()

if len(os.listdir(EMOJI_PATH_SVG)) == 0:
    extract_emojis()

else:
    print('emojis.zip already extracted')
