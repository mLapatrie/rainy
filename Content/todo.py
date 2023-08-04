from PIL import Image, ImageDraw, ImageFont
from Content import write

file = open("Content/App files/todo.txt", "r")

todoList = []

currentInd = 0

showDone = False

def main(oled, draw):
    global todoList
    global currentInd
    
    getTodos()
    
    fontSize = 25
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    if len(todoList)-1 >= currentInd >= 0:
        currentTodo = todoList[currentInd][0]
    else:
        currentTodo = "New todo"
    
    (font_width, font_height) = font.getsize(currentTodo)
    while font_width > 100:
        fontSize -= 1
        font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=fontSize)
        (font_width, font_height) = font.getsize(currentTodo)
        
    draw.text(
        (oled.width // 2 - font_width // 2 + 10, oled.height // 2 - font_height // 2 - 3),
        currentTodo,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    indexIndicator = str(currentInd + 1)+"/"+str(len(todoList))
    
    (font_width, font_height) = font.getsize(indexIndicator)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 23),
        indexIndicator,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=13)
    
    (font_width, font_height) = font.getsize("To do")
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 26),
        "To do",
        font=font,
        fill=255,
    )
    
    # done circle
    draw.arc([(2, 24), (18, 40)], start=0, end=360, fill=255)
    
    # done check
    if currentTodo == "New todo":
        draw.line([(6,32),(14,32)], fill=255)
        draw.line([(10,28),(10,36)], fill=255)
    else:
        if todoList[currentInd][1] == "d":
            draw.line([(2,24),(18,40)], fill=255)
            draw.line([(2,40),(18,24)], fill=255)
    
    # up
    draw.polygon([(118,5), (122,1), (126,5)], fill=255)
    
    # down
    draw.polygon([(118,58), (122,62), (126,58)], fill=255)
    
    return 0


def loop(oled, draw):
    
    return 0


def left(oled, draw):
    # does nothing
    return "todo"


def up(oled, draw):
    global currentInd
    
    if currentInd >= 0:
        currentInd -= 1
        
    main(oled, draw)
    
    return "todo"


def right(oled, draw):
    # does nothing
    return "todo"


def down(oled, draw):
    global currentInd
    
    if currentInd <= len(todoList) - 1:
        currentInd += 1
        
    main(oled, draw)
    
    return "todo"


def center(oled, draw):
    global todoList
    global currentInd
    global file
    
    if len(todoList) - 1 >= currentInd >= 0:
        if todoList[currentInd][1] == "n":
            todoList[currentInd][1] = "d"
        else:
            todoList[currentInd][1] = "n"
        
        file.close()
        
        file = open("Content/App files/todo.txt", "w")
        
        content = ""
        for i in todoList:
            content += i[0]+"^"+i[1]+"\n"
        file.write(content)
        
        file.close()
    else:
        return "write"
    
    todoList = []
    
    file = open("Content/App files/todo.txt", "r")
        
    main(oled, draw)
    
    return "todo"


def back(oled, draw):
    
    return "apps"


def getTodos():
    global file
    global todoList
    
    for line in file:
        part = line.rstrip().partition("^")
        if part[2] == "n":
            todoList.append([part[0], part[2]])
    

def getText(oled, draw):
    global currentInd
    global todoList
    global file
    
    newTodo = write.getInputString()
    
    if currentInd == -1:
        todoList.insert(0, [newTodo, "n"])
        currentInd = 0
    elif currentInd == len(todoList):
        todoList.append([newTodo, "n"])
        currentInd = len(todoList) - 1
        
    file.close()
        
    file = open("Content/App files/todo.txt", "w")
    
    content = ""
    for i in todoList:
        content += i[0]+"^"+i[1]+"\n"
    file.write(content)
    
    file.close()
    
    todoList = []
    
    file = open("Content/App files/todo.txt", "r")
    
    main(oled, draw)


