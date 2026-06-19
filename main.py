from Backend.agent import Agent
from fontTools.ttLib import TTFont
from PIL import Image


FONT_PATH = "Backend/Assets/NotoColorEmoji-Regular.ttf"

font = TTFont(FONT_PATH)
cmap = font.getBestCmap()
emojis = [chr(code) for code in cmap.keys()]
font.close()

im = Image.open("test_image.jpg")

agent = Agent(im, FONT_PATH, emojis, 20)
im = agent.place_random_emoji()
for i, x in enumerate(range(100)):
    a = Agent(im, FONT_PATH, emojis, 20)
    im = a.place_random_emoji()
    print(f"{i+1}/100")
im.show()

