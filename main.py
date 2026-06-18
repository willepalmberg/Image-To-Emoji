from Backend.agent import Agent
from fontTools.ttLib import TTFont
from PIL import Image

FONT_PATH = "Backend/Assets/NotoColorEmoji-Regular.ttf"

font = TTFont("your_font.ttf")
cmap = font.getBestCmap()
characters = [chr(code) for code in cmap.keys()]

im = Image.open("test_image.jpg")

agent = Agent(im, font, 20)
agent.place_random_emoji()