from Backend.agent import Agent
from PIL import Image

FONT_PATH = "Backend/Assets/NotoColorEmoji-Regular.ttf"

im = Image.open("test_image.jpg")

agent = Agent(im, FONT_PATH, 20)
agent.place_random_emoji()