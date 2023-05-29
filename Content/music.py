from PIL import Image, ImageDraw, ImageFont
from os import listdir
from os.path import isfile, join
import vlc


path = "Content/Music"

myMusic = [f for f in listdir(path) if isfile(join(path,f))]

mediaPlayer = vlc.MediaPlayer()

currentInd = 0

playingInd = 0
playing = False
paused = False


def main(oled, draw):
    global myMusic
    global currentInd
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    currentMusic = myMusic[currentInd]
    
    (font_width, font_height) = font.getsize(currentMusic)
    if font_width > 100:
        while font_width > 100:
            currentMusic = currentMusic[:-1]
            (font_width, font_height) = font.getsize(currentMusic)
            
    draw.text(
        (oled.width // 2 - font_width // 2 + 10, oled.height // 2 - font_height // 2 - 3),
        currentMusic,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    indexIndicator = str(currentInd + 1)+"/"+str(len(myMusic))
    
    (font_width, font_height) = font.getsize(indexIndicator)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 23),
        indexIndicator,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    
    (font_width, font_height) = font.getsize("Music")
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 26),
        "Music",
        font=font,
        fill=255,
    )
    
    if currentInd == playingInd and playing:
        # pause button
        draw.line([(5,24),(5,40)], width=4, fill=255)
        draw.line([(13,24),(13,40)], width=4, fill=255)
    else:
        # play arrow
        draw.polygon([(2,24),(2,40),(13,32)], fill=255)
    
    # up
    draw.polygon([(118,5), (122,1), (126,5)], fill=255)
    
    # down
    draw.polygon([(118,58), (122,62), (126,58)], fill=255)
    
    return 0


def loop(oled, draw):
    
    return 0


def left(oled, draw):
    # does nothing
    return "music"


def up(oled, draw):
    global currentInd
    
    if currentInd > 0:
        currentInd -= 1
        
    main(oled, draw)
    
    return "music"


def right(oled, draw):
    # does nothing
    return "music"


def down(oled, draw):
    global currentInd
    
    if currentInd < len(myMusic) - 1:
        currentInd += 1
        
    main(oled, draw)
    
    return "music"


def center(oled, draw):
    global myMusic
    global currentInd
    global playingInd
    global playing
    global paused
    global mediaPlayer
    
    if not playing and not paused:
        media = vlc.Media(join(path, myMusic[currentInd]))
        mediaPlayer.set_media(media)
        mediaPlayer.play()
        mediaPlayer.set_pause(0)
        playing = True
        playingInd = currentInd
    elif playing and currentInd == playingInd:
        mediaPlayer.set_pause(1)
        playing = False
        paused = True
    elif currentInd == playingInd and paused:
        mediaPlayer.set_pause(0)
        playing = True
        paused = False
    elif currentInd != playingInd:
        media = vlc.Media(join(path, myMusic[currentInd]))
        mediaPlayer.set_media(media)
        mediaPlayer.play()
        mediaPlayer.set_pause(0)
        playingInd = currentInd
        playing = True
        pause = False
    
    
    main(oled, draw)
    
    return "music"


def back(oled, draw):
    
    return "apps"

   