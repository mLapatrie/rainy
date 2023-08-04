from PIL import Image, ImageDraw, ImageFont

globalAppArray = []
currentInd = 0


def main(oled, draw):
    global currentInd
    global globalAppArray
    
    fontSize = 25
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(globalAppArray[currentInd])
    while font_width > 122:
        fontSize -= 1
        font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
        (font_width, font_height) = font.getsize(globalAppArray[currentInd])
        
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 10),
        globalAppArray[currentInd],
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    indexIndicator = str(currentInd + 1)+"/"+str(len(globalAppArray))
    
    (font_width, font_height) = font.getsize(indexIndicator)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 23),
        indexIndicator,
        font=font,
        fill=255,
    )
    
    # right arrow
    draw.polygon([(123,53),(127,57),(123,61)], fill=255)
    
    # left arrow
    draw.polygon([(4,61),(0,57),(4,53)], fill=255)
    
    return 0
    

def loop(oled, draw):
    return 0
    

def left(oled, draw):
    global currentInd
    
    if currentInd > 0:
        currentInd -= 1
    else:
        currentInd = len(globalAppArray) - 1
        
    main(oled, draw)
    
    return "apps"

    
def up(oled, draw):
    # does nothing
    return "apps"

    
def right(oled, draw):
    global currentInd
    
    if currentInd < len(globalAppArray) - 1:
        currentInd += 1
    else:
        currentInd = 0
    
    main(oled, draw)
    
    return "apps"

    
def down(oled, draw):
    # does nothing
    return "apps"
    

def center(oled, draw):
    # selects app
    global globalAppArray
    return globalAppArray[currentInd]
    
    
def back(oled, draw):
    return "clock"


def setApps(appArray):
    global globalAppArray
    globalAppArray = appArray
    
    
    