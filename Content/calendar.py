from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

file = open("Content/App files/calendar.txt", "r")

days = []
content = []

timeInd = 0
dayInd = 0

for line in file:
    if line == "\n":
        days.append(content)
        content = []
    else:
        content.append(line.rstrip())
    
days.append(content)


def main(oled, draw):
    global days
    global timeInd
    global dayInd
    
    dayName = days[dayInd][0]
    timeDetails = days[dayInd][1 + 2*timeInd]
    description = days[dayInd][2 + 2*timeInd].partition("-")[0]
    extraInfo = days[dayInd][2 + 2*timeInd].partition("-")[2]
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(description)
    
    if font_width > 100:
        while font_width > 100:
            description = description[:-1]
            (font_width, font_height) = font.getsize(description)
        description += "..."
        (font_width, font_height) = font.getsize(description)
    
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 8),
        description,
        font=font,
        fill=255,
    )
    
    (font_width, font_height) = font.getsize(extraInfo)
    
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 8),
        extraInfo,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    (font_width, font_height) = font.getsize(timeDetails)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 23),
        timeDetails,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    
    (font_width, font_height) = font.getsize(dayName)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 26),
        dayName,
        font=font,
        fill=255,
    )
    
    # up
    draw.polygon([(118,53), (122,49), (126,53)], fill=255)
    
    # down
    draw.polygon([(118,58), (122,62), (126,58)], fill=255)

    # right arrow
    draw.polygon([(123,1),(127,5),(123,9)], fill=255)
    
    # left arrow
    draw.polygon([(4,9),(0,5),(4,1)], fill=255)
    
    return 0


def loop(oled, draw):
    
    return 0


def left(oled, draw):
    global dayInd
    global timeInd
    
    if dayInd > 0:
        dayInd -= 1
        timeInd = 0
        
    main(oled, draw)
    
    return "calendar"


def up(oled, draw):
    global timeInd
    
    if timeInd > 0:
        timeInd -= 1
        
    main(oled, draw)
    
    return "calendar"


def right(oled, draw):
    global dayInd
    global timeInd
    
    if dayInd < len(days)-1:
        dayInd += 1
        timeInd = 0
        
    main(oled, draw)
    
    return "calendar"


def down(oled, draw):
    global timeInd
    
    if timeInd < (len(days[dayInd]) - 1)/2 - 1:
        timeInd += 1
        
    main(oled, draw)
    
    return "calendar"


def center(oled, draw):
    
    return "calendar"


def back(oled, draw):
    
    return "apps"


def getIndexes():
    global dayInd
    
    currentDay = datetime.now().weekday()
    
    if currentDay <= len(days)-1:
        dayInd = currentDay
    

getIndexes()
    
    

