from PIL import Image, ImageDraw, ImageFont
import time


# timer
timerValues = [0, 0, 0, 0, 0, 0] # 00:00:00
timerStartValue = 0
modifyingInd = 0
modifying = False
running = False
startTimeTR = 0


def main(oled, draw):
    global current
    
    up(oled, draw)


def loop(oled, draw):
    if running:
        changeTimerText(oled, draw)


def left(oled, draw):
    global modifyingInd
    global modifying
    
    if modifyingInd > 0:
        modifyingInd -= 1
        modifying = False
        up(oled, draw)
    
    return "timer"
    
def up(oled, draw):
    global timerValues
    global modifyingInd
    global modifying
    
    # show timer
    
    if modifying:
        if modifyingInd == 0 or modifyingInd == 2 and timerValues[modifyingInd] < 5:
            timerValues[modifyingInd] += 1
        elif modifyingInd == 1 or modifyingInd == 3 or modifyingInd == 4 or modifyingInd == 5 and timerValues[modifyingInd] < 9:
            timerValues[modifyingInd] += 1
    elif not modifying and not running:
        modifying = True
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=25)
    
    draw.rectangle([(0,0), (128,64)], fill=0)
    
    timer = "{:1}{:2}:{:3}{:4}:{:5}{:6}".format(timerValues[0], timerValues[1], timerValues[2], timerValues[3], timerValues[4], timerValues[5]).replace(" ", "")
    
    if not running:
        if modifyingInd == 0:
            draw.line([(5, 48),(18, 48)], fill=255, width=2)
        elif modifyingInd == 1:
            draw.line([(20, 48),(33, 48)], fill=255, width=2)
        elif modifyingInd == 2:
            draw.line([(50, 48),(63, 48)], fill=255, width=2)
        elif modifyingInd == 3:
            draw.line([(65, 48),(78, 48)], fill=255, width=2)
        elif modifyingInd == 4:
            draw.line([(95, 48),(108, 48)], fill=255, width=2)
        elif modifyingInd == 5:
            draw.line([(110, 48),(123, 48)], fill=255, width=2)
        
    
    (font_width, font_height) = font.getsize(timer)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        timer,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    (font_width, font_height) = font.getsize("timer")
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 20),
        "timer",
        font=font,
        fill=255,
    )
    
    # back arrow
    draw.arc(((112,48),(125,61)), start=225, end=45, fill=255)
    draw.polygon([(112,48),(112,52),(116,52)], fill=255)
    
    # center arrow
    draw.arc(((59, 50),(69, 60)), start=0, end=360, fill=255)
    draw.arc(((62, 53),(66, 57)), start=0, end=360, fill=255, width=4)
    
        
    return "timer"


def right(oled, draw):
    global modifyingInd
    global modifying
    
    if modifyingInd < 5:
        modifyingInd += 1
        modifying = False
        up(oled, draw)
    
    return "timer"
    

def down(oled, draw):
    global modifying
    global modifyingInd
    global timerValues
        
    if modifying:
        if timerValues[modifyingInd] > 0:
            timerValues[modifyingInd] -= 1
            modifying = False
            up(oled, draw)
    
    return "timer"
    
    
def center(oled, draw):
    global running
    global modifying
        
    timer(not running)
    modifying = False
    up(oled, draw)
    
    return "timer"
    
    
def back(oled, draw):
    global modifying
    
    modifying = False
    
    return "apps"


def timer(start):
    global running
    global timerValues
    global startTimeTR
    global timerStartValues
    
    running = start
    
    if start:
        startTimeTR = time.time()
        timerStartValues = round(timerValues[0] * 600 + timerValues[1] * 60 + timerValues[2] * 10 + timerValues[3] + timerValues[4] / 10 + timerValues[5] / 100, 2)
        
    
def changeTimerText(oled, draw):
    global timerValues
    global startTimeTR
    global timerStartValues
    
    modifying = False
    
    totalTime = timerStartValues - round(time.time()-startTimeTR,2)
    
    if totalTime > 0:
        part = str(totalTime).partition(".")
        
        timerValues[5] = int(part[2][:2].zfill(2)[1])
        timerValues[4] = int(part[2][:2].zfill(2)[0])
        m, s = divmod(int(part[0]), 60)
        s = str(s).zfill(2)
        m = str(m).zfill(2)
        
        timerValues[3] = int(s[1])
        timerValues[2] = int(s[0])
        timerValues[1] = int(m[1])
        timerValues[0] = int(m[0])
        
    else:
        timerValues = [0, 0, 0, 0, 0, 0]
        timerStartValues = 0
        running = False
    
    up(oled, draw)
        
    
