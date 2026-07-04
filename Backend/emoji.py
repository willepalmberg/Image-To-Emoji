from resvg_py import svg_to_bytes
from zipfile import ZipFile
from random import randint
from requests import get
from io import BytesIO
from PIL import Image

import shutil
import sys
import cv2
import os

# Här får vi våra svg emojis ifrån
TWEMOJI_URL = "https://github.com/twitter/twemoji/archive/refs/tags/v14.0.2.zip"
TWEMOJI_SVGS_PATH = 'twemoji-14.0.2/assets/svg/'

class Emoji:
    def __init__(self, emoji_size: int, emoji_path_svg: str, emoji_path_png: str):
        self.emoji_size = emoji_size
        self.emoji_path_svg = emoji_path_svg
        self.emoji_path_png = emoji_path_png

        self.emojis = []

    # Från https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
    def download_emojis(self):
        with open('emojis.zip', "wb") as f:
            print("Downloading %s" % 'emojis.zip')
            response = get(TWEMOJI_URL, stream=True)
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

    def extract_emojis(self):
        os.makedirs(self.emoji_path_png, exist_ok=True)
        print(f'Extracting emojis.zip to {self.emoji_path_svg}')

        if not os.path.exists(self.emoji_path_svg):
            os.makedirs(self.emoji_path_svg)

        z = ZipFile('emojis.zip')

        for file in z.namelist():
            if file.startswith(TWEMOJI_SVGS_PATH) and file != TWEMOJI_SVGS_PATH:
                filename = os.path.basename(file)
                if filename:
                    target_path = os.path.join(self.emoji_path_svg, filename)
                    with z.open(file) as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

    def convert_svgs_to_pngs(self):
        os.makedirs(self.emoji_path_png, exist_ok=True)

        svg_files = [f for f in os.listdir(self.emoji_path_svg) if f.endswith('.svg')]
        total = len(svg_files)

        for i, filename in enumerate(svg_files):

            svg_path = os.path.join(self.emoji_path_svg, filename)
            png_path = os.path.join(self.emoji_path_png, filename.replace('.svg', '.png'))

            png_bytes = svg_to_bytes(svg_path=svg_path, width=self.emoji_size, height=self.emoji_size)
            rendered_img = Image.open(BytesIO(bytes(png_bytes))).convert('RGBA')

            if rendered_img.size == (self.emoji_size, self.emoji_size):
                rendered_img.save(png_path)

            else:
                canvas = Image.new('RGBA', (self.emoji_size, self.emoji_size), (0, 0, 0, 0))
                paste_x = (self.emoji_size - rendered_img.width) // 2
                paste_y = (self.emoji_size - rendered_img.height) // 2
                canvas.paste(rendered_img, (paste_x, paste_y), rendered_img)
                canvas.save(png_path)

            print(f'({i + 1}/{total}) | {filename} converted to PNG')

    def load_emojis_to_memory(self):
        emojis = []
        for filename in os.listdir(self.emoji_path_png):
            if filename.endswith('.png'):
                emoji_path = os.path.join(self.emoji_path_png, filename)
                emoji = cv2.imread(emoji_path)
                emojis.append(Image.fromarray(emoji))

        self.emojis = emojis

    def grab_random_emoji(self):
        return self.emojis[randint(0, len(self.emojis) - 1)]
