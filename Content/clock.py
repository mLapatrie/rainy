from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


time = "00:00"
date = "07/21"

current = 0


def main(oled, draw):
    global time
    global date
    
    getTime(oled, draw)
    
    left(oled, draw)
    

def loop(oled, draw):
    getTime(oled, draw)
        

def getTime(oled, draw):
    global time
    global date
    global current
    
    pTimeM = time[-2:]
    pDay = date[-2:]
    
    now = datetime.now()
    time = now.strftime("%H:%M")
    date = datetime.now().strftime("%m/%d")
    
    if current == 0 and time[-2:] != pTimeM:
        left(oled, draw)
    elif current == 1 and date[-2:] != pDay:
        right(oled, draw)


def left(oled, draw):
    global time
    global current
    
    current = 0
    
    # show time
    
    font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=40)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(time)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 10),
        time,
        font=font,
        fill=255,
    )
    
    # right arrow
    draw.polygon([(123,53),(127,57),(123,61)], fill=255)
    
    return "clock"


def up(oled, draw):
    
    return "timer"


def right(oled, draw):
    global date
    global current
    
    current = 1
    
    # show date
    
    font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=40)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(date)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 8),
        date,
        font=font,
        fill=255,
    )
    
    # left arrow
    draw.polygon([(4,61),(0,57),(4,53)], fill=255)

    return "clock"
    

def down(oled, draw):
    return "stopwatch"
    

def center(oled, draw):
    # opens apps
    return "apps"


def back(oled, draw):
    # does nothing
    return "clock"