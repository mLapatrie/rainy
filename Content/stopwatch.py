from PIL import Image, ImageDraw, ImageFont
import time


# stopwatch
counting = False
stopwatchText = "00:00:00 "
startTimeSW = 0


def main(oled, draw):
    global current
    
    down(oled, draw)


def loop(oled, draw):
    if counting:
        changeStopwatchText(oled, draw)


def left(oled, draw):
    return "stopwatch"
    
def up(oled, draw):
    return "stopwatch"


def right(oled, draw):
    return "stopwatch"
    

def down(oled, draw):
    global stopwatchText
    
    # show stopwatch
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=25)
    
    draw.rectangle([(0,0), (128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(stopwatchText[:-1])
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        stopwatchText,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    (font_width, font_height) = font.getsize("stopwatch")
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 20),
        "stopwatch",
        font=font,
        fill=255,
    )
    
    # back arrow
    draw.arc(((112,48),(125,61)), start=225, end=45, fill=255)
    draw.polygon([(112,48),(112,52),(116,52)], fill=255)
    
    # center arrow
    draw.arc(((59, 50),(69, 60)), start=0, end=360, fill=255)
    draw.arc(((62, 53),(66, 57)), start=0, end=360, fill=255, width=4)
    
    return "stopwatch"
    
    
def center(oled, draw):
    global counting
    
    stopwatch(not counting)
    down(oled, draw)
    
    return "stopwatch"
    
    
def back(oled, draw):
    return "apps"
    

def stopwatch(start):
    global counting
    global stopwatchText
    global startTimeSW
    
    counting = not counting
    
    if start:
        startTimeSW = time.time()


def changeStopwatchText(oled, draw):
    global stopwatchText
    global startTimeSW
    
    totalTime = round(time.time()-startTimeSW,2)
    
    part = str(totalTime).partition(".")
    
    ms = part[2]
    m, s = divmod(int(part[0]), 60)
    m = str(m)
    s = str(s)
    
    
    stopwatchText = "{:1}:{:2}:{:3}".format(m.zfill(2), s.zfill(2), ms.zfill(2))
    down(oled, draw)

