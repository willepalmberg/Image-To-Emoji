from PIL import Image, Image

class Agent:
    def __init__(self, image, emoji_font):
        self.image = image
        self.final_image = None
        self.font = emoji_font
