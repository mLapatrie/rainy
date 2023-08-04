from PIL import Image, ImageDraw, ImageFont

characters = ['abcdefghijklmnopqrstuvwxyz1234567890-=:/".,¤', "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%?&*()+_;[]{} "]
charactersInd = 0
currentInd = 0

inputString = ""


def main(oled, draw):
    global characters
    global charactersInd
    global currentInd
    global inputString
    
    font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=30)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(characters[charactersInd][currentInd])
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 20),
        characters[charactersInd][currentInd],
        font=font,
        fill=255,
    )
    
    # underline
    draw.line([(55, 32),(73, 32)], fill=255)
    
    # left
    draw.polygon([(41,26),(37,22),(41,18)], fill=255)
    
    # right
    draw.polygon([(46,18),(50,22),(46,26)], fill=255)
    
    # up
    draw.polygon([(78,19), (82,15), (86,19)], fill=255)
    
    # down
    draw.polygon([(78,24), (82,28), (86,24)], fill=255)
    
    font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=20)
    
    (font_width, font_height) = font.getsize("¤")
    draw.text(
        (oled.width // 2 - font_width // 2 + 33, oled.height // 2 - font_height // 2 - 15),
        "¤",
        font=font,
        fill=255,
    )
    
    # input string
    fontSize = 15
    
    font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
    
    (font_width, font_height) = font.getsize(inputString)
    while font_width > 122:
        fontSize -= 1
        font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
        (font_width, font_height) = font.getsize(inputString)
        
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 20),
        inputString,
        font=font,
        fill=255,
    )
    
    return 0


def loop(oled, draw):
    
    return 0


def left(oled, draw):
    global currentInd
    
    if currentInd > 0:
        currentInd -= 1
    else:
        currentInd = len(characters[0]) - 1
        
    main(oled, draw)
    
    return "write"


def up(oled, draw):
    global charactersInd
    
    if charactersInd == 0:
        charactersInd = 1
    else:
        charactersInd = 0
        
    main(oled, draw)
    
    return "write"


def right(oled, draw):
    global currentInd
    
    if currentInd < len(characters[0]) - 1:
        currentInd += 1
    else:
        currentInd = 0
        
    main(oled, draw)
    
    return "write"


def down(oled, draw):
    global charactersInd
    
    if charactersInd == 1:
        charactersInd = 0
    else:
        charactersInd = 1
        
    main(oled, draw)
    
    return "write"


def center(oled, draw):
    global characters
    global charactersInd
    global currentInd
    global inputString
    
    # adds current input to input string
    if charactersInd == 0 and currentInd == len(characters[charactersInd]) - 1:
        # returns text to sender
        charactersInd = 0
        currentInd = 0
        
        return 0
    else:
        inputString += characters[charactersInd][currentInd]
    
        main(oled, draw)
    
        return "write"


def back(oled, draw):
    global inputString
    
    # removes the last inputed char
    inputString = inputString[:-1]
    
    main(oled, draw)
    
    return "write"


def getInputString():
    global inputString
    
    returnString = inputString
    inputString = ""
    
    return returnString