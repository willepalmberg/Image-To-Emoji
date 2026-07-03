from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from random import randint, choice


class Agent:
    def __init__(self, image: Image.Image, font, emojis: list[str], emoji_size):
        self.image = image.copy().convert("RGBA")
        self.emojis = emojis
        self.font_path = font
        self.font_size = emoji_size
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        self.emoji_width, self.emoji_height = self._measure_emoji_size()

    def _measure_emoji_size(self) -> tuple[int, int]:
        scratch = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(scratch)
        sample = self.emojis[0]
        bbox = draw.textbbox((0, 0), sample, font=self.font, embedded_color=True)
        return int(bbox[2]) - int(bbox[0]), int(bbox[3]) - int(bbox[1])

    def place_random_emoji(self) -> Image.Image:
        image = self.image
        chosen = choice(self.emojis).strip()

        randx = randint(0, max(image.width - self.emoji_width, 0))
        randy = randint(0, max(image.height - self.emoji_height, 0))

        with Pilmoji(image) as pilmoji:
            pilmoji.text((randx, randy), chosen, (0, 0, 0), self.font)

        self.image = image
        return image