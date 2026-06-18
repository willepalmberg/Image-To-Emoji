from PIL import Image, ImageFont, ImageText
from random import randint, choice
from string import ascii_letters


class Agent:
    def __init__(self, image: Image.Image, emoji_font, emoji_size):
        self.image = image
        self.final_image = None
        self.font = emoji_font
        self.font_size = emoji_size

        self.letters = ascii_letters

    def place_random_emoji(self) -> Image.Image:
        if self.final_image is not None:
            return self.final_image

        image = self.image.copy()
        im_font = ImageFont.truetype(self.font, self.font_size)
        text = ImageText.Text(choice(self.letters), im_font)
        text.embed_color()
        text.stroke(2, "#0f0")
        im_text = Image.new("RGB", text.get_bbox()[2:])
        image.paste(im_text, (randint(0, image.width - im_text.width), randint(0, image.height - image.height)))
        image.show()
        return Image

