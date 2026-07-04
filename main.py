from Backend.emoji import Emoji
from PIL import Image
from random import randint
import os


EMOJI_PATH_SVG = 'Backend/Assets/Emojis_SVG'
EMOJI_PATH_PNG = 'Backend/Assets/Emojis_PNG'

EMOJI_SIZE = 16

emoji = Emoji(EMOJI_SIZE, EMOJI_PATH_SVG, EMOJI_PATH_PNG)

if os.path.isfile('emojis.zip'):
    print("emojis.zip already exists")
else:
    print("emojis.zip does not exist")
    emoji.download_emojis()

if not os.path.exists(EMOJI_PATH_SVG):
    os.makedirs(EMOJI_PATH_SVG)

if len(os.listdir(EMOJI_PATH_SVG)) == 0:
    emoji.extract_emojis()

else:
    print('emojis.zip already extracted')

if not os.path.exists(EMOJI_PATH_PNG):
    os.makedirs(EMOJI_PATH_PNG)

if len(os.listdir(EMOJI_PATH_PNG)) == 0:
    emoji.convert_svgs_to_pngs()

print(f'Loading emojis into memory...')
emoji.load_emojis_to_memory()


im = Image.open('test_image.jpg').convert('RGBA')
for i in range(100):
    em = emoji.grab_random_emoji()

    x, y = randint(0, im.width - EMOJI_SIZE), randint(0, im.height - EMOJI_SIZE)

    im.paste(em, (x, y))

im.show()
