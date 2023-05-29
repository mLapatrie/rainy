
from Content import *

with open("Content/App files/apps.txt") as file:
    appNames = file.readlines()

apps.setApps(appNames)
current = "music"
writer = ""


import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from time import sleep
import random


buttonLeft = digitalio.DigitalInOut(board.D5)
buttonLeft.direction = digitalio.Direction.INPUT
buttonLeft.pull = digitalio.Pull.UP

buttonUp = digitalio.DigitalInOut(board.D6)
buttonUp.direction = digitalio.Direction.INPUT
buttonUp.pull = digitalio.Pull.UP

buttonRight = digitalio.DigitalInOut(board.D13)
buttonRight.direction = digitalio.Direction.INPUT
buttonRight.pull = digitalio.Pull.UP

buttonDown = digitalio.DigitalInOut(board.D19)
buttonDown.direction = digitalio.Direction.INPUT
buttonDown.pull = digitalio.Pull.UP

buttonCenter = digitalio.DigitalInOut(board.D26)
buttonCenter.direction = digitalio.Direction.INPUT
buttonCenter.pull = digitalio.Pull.UP

buttonBack = digitalio.DigitalInOut(board.D25)
buttonBack.direction = digitalio.Direction.INPUT
buttonBack.pull = digitalio.Pull.UP


ledGreen1 = digitalio.DigitalInOut(board.D12)
ledGreen1.direction = digitalio.Direction.OUTPUT

ledGreen2 = digitalio.DigitalInOut(board.D16)
ledGreen2.direction = digitalio.Direction.OUTPUT

ledYellow = digitalio.DigitalInOut(board.D20)
ledYellow.direction = digitalio.Direction.OUTPUT

ledRed = digitalio.DigitalInOut(board.D21)
ledRed.direction = digitalio.Direction.OUTPUT


i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.show()

image = Image.new('1', (oled.width, oled.height))

font= ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=35)

draw = ImageDraw.Draw(image)
oled.show()


def startAnimation():
    draw.rectangle([(0, 0), (128, 64)], fill=255)
        
    rainPosX = [0] * oled.width
    for idx, posX in enumerate(rainPosX):
        rainPosX[idx] = idx
            
    rainPosY = [0] * oled.width
    for idx, posY in enumerate(rainPosY):
        rainPosY[idx] = random.randint(0, 100) - 100
    rainPosY[0] = -100
            
    t = 0
        
    while True:
        if rainPosY[0] > 64:
            sleep(0.2)
            break
            
        for i in rainPosX:
            draw.point((i, rainPosY[i]), fill=0)
                
            rainPosY[i] += 1/2 * 9.81 * t * t
            draw.point((i, rainPosY[i]), fill=255)
            
            
        (font_width, font_height) = font.getsize("rainy")
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            "rainy",
            font=font,
            fill=0,
        )
            
        oled.image(image)
        oled.show()
        
        t += 0.01
        sleep(0.01)
    
    draw.rectangle([(0,0),(128,64)],fill=0)
    
    oled.image(image)
    oled.show()


#startAnimation()

eval(current+".main(oled, draw)")

oled.image(image)
oled.show()

# main loop
pLeft = True
pUp = True
pRight = True
pDown = True
pCenter = True
pBack = True

rainPosX = random.randint(0, 127)
rainPosY = 0

v0 = 0
t = 0

pPixel = 0
showRain = True

n = 0

while True:
    n += 1
    
    eval(current+".loop(oled, draw)")
    
    oled.image(image)
    oled.show()
    
    if showRain:
        if pPixel == 0:
            draw.point((rainPosX, rainPosY), fill=0)
        
        if rainPosY > 1000:
            rainPosX = random.randint(0,127)
            rainPosY = 0
            t = 0
        
        rainPosY = v0 * t + 1/2 * 9.81 * t * t
        
        t += 0.1
        
        if rainPosY < 64:
            pPixel = image.getpixel((rainPosX, rainPosY))
        
        if pPixel == 0:
            draw.point((rainPosX, rainPosY), fill=255)
        
        oled.image(image)
        oled.show()
    
    
    if not buttonLeft.value and pLeft:
        screen = eval(current+".left(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
            else:
                eval(screen+".main(oled, draw)")
            current = screen
            
        oled.image(image)
        oled.show()
        pLeft = False
    elif not buttonUp.value and pUp:
        screen = eval(current+".up(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
            else:
                eval(screen+".main(oled, draw)")
            current = screen
        
        oled.image(image)
        oled.show()
        pUp = False
    elif not buttonRight.value and pRight:
        screen = eval(current+".right(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
            else:
                eval(screen+".main(oled, draw)")
            current = screen
            
        oled.image(image)
        oled.show()
        pRight = False
    elif not buttonDown.value and pDown:
        screen = eval(current+".down(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
            else:
                eval(screen+".main(oled, draw)")
            current = screen
            
        oled.image(image)
        oled.show()
        pDown = False
    elif not buttonCenter.value and pCenter:
        screen = eval(current+".center(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
                current = screen
            elif screen == 0:
                eval(writer+".getText(oled, draw)")
                current = writer
            else:
                eval(screen+".main(oled, draw)")
                current = screen
            
            
        oled.image(image)
        oled.show()
        pCenter = False
    elif not buttonBack.value and pBack:
        screen = eval(current+".back(oled, draw)")
        if screen != current:
            if screen == "write" and current != "write":
                writer = current
                write.main(oled, draw)
            else:
                eval(screen+".main(oled, draw)")
            current = screen
            
        oled.image(image)
        oled.show()
        pBack = False
    
    if buttonLeft.value:
        pLeft = True
    if buttonUp.value:
        pUp = True
    if buttonRight.value:
        pRight = True
    if buttonDown.value:
        pDown = True
    if buttonCenter.value:
        pCenter = True
    if buttonBack.value:
        pBack = True
