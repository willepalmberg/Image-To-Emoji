from PIL import Image, ImageFont, ImageText, ImageDraw
from pilmoji import Pilmoji
from random import randint, choice


class Agent:
    def __init__(self, image: Image.Image, font, emojis: list[str], emoji_size):
        self.image = image
        self.final_image = None
        self.emojis = emojis
        self.font_path = font
        self.font_size = emoji_size

        self.font = ImageFont.truetype(self.font_path, self.font_size)


    def place_random_emoji(self) -> Image.Image:
        image = self.image.copy().convert("RGBA")

        chosen = choice(self.emojis)

        randx = randint(0, image.width - self.font_size)
        randy = randint(0, image.height - self.font_size)

        with Pilmoji(image) as pilmoji:
            pilmoji.text((randx, randy), chosen.strip(), (0, 0, 0), self.font)

        self.image = image

