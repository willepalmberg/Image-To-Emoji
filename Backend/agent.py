from PIL import Image, ImageFont, ImageText, ImageDraw
from pilmoji import Pilmoji
from random import randint, choice
from string import ascii_letters


class Agent:
    def __init__(self, image: Image.Image, font, emojis: list[str], emoji_size):
        self.image = image
        self.final_image = None
        self.emojis = emojis
        self.font = font
        self.font_size = emoji_size

        self.letters = ascii_letters

    def place_random_emoji(self) -> Image.Image:
        image = self.image.copy().convert("RGBA")

        font = ImageFont.truetype(self.font, self.font_size)
        chosen = choice(self.emojis)

        with Pilmoji(image) as pilmoji:
            pilmoji.text((10, 10), chosen.strip(), (0, 0, 0), font)

        return image

