from PIL import Image, ImageDraw, ImageFont
import datetime

lines = []
with open("Content/App files/routes.txt") as file:
    lines = [line.rstrip() for line in file]

schedules = []
data = []
routes = []

currentIndexes = [0, 0]

detailedForwardRoutes = []
detailedBackwardRoutes = []
detailedRoutes = []

currentRouteIndex = 0


def main(oled, draw):
    global routes
    global currentRouteIndex
    global currentForwardIndex
    global currentBackwardIndex
    global detailedForwardRoutes
    global detailedBackwardRoutes
    
    currentRoute = detailedRoutes[currentRouteIndex][currentIndexes[currentRouteIndex]].split("-")
    busName = currentRoute[0]
    currentRoute.pop(0)
    currentRoute = "-".join(currentRoute)
    
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=15)
    
    draw.rectangle([(0,0),(128,64)], fill=0)
    
    (font_width, font_height) = font.getsize(busName)
    
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 10),
        busName,
        font=font,
        fill=255,
    )
    
    (font_width, font_height) = font.getsize(currentRoute)
    
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 + 5),
        currentRoute,
        font=font,
        fill=255,
    )
    
    font = ImageFont.truetype("Content/Fonts/SpaceMono-Regular.ttf", size=12)
    
    (font_width, font_height) = font.getsize("Refresh")
    
    draw.text(
        (oled.width // 2 - font_width // 2 + 13, oled.height // 2 - font_height // 2 + 22),
        "Refresh",
        font=font,
        fill=255,
    )
    
    (font_width, font_height) = font.getsize(routes[currentRouteIndex][0])
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2 - 26),
        routes[currentRouteIndex][0],
        font=font,
        fill=255,
    )
    
    # refresh circle
    draw.arc([(37, 52),(47, 62)], start=0, end=360, fill=255)
    draw.arc([(41, 56),(44, 59)], start=0, end=360, fill=255, width=4)
    
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
    global currentRouteIndex
    
    if currentRouteIndex > 0:
        currentRouteIndex -= 1
    
    main(oled, draw)
    
    return "bus"


def up(oled, draw):
    global currentIndexes
    global currentRouteIndex
    global detailedRoutes
    
    if currentIndexes[currentRouteIndex] < len(detailedRoutes[currentRouteIndex])-1:
        currentIndexes[currentRouteIndex] += 1
        
    main(oled, draw)
    
    return "bus"


def right(oled, draw):
    global currentRouteIndex
    global routes
    
    if currentRouteIndex < len(routes)-1:
        currentRouteIndex += 1
        
    main(oled, draw)
    
    return "bus"


def down(oled, draw):
    global currentIndexes
    global currentRouteIndex
    
    if currentIndexes[currentRouteIndex] > 0:
        currentIndexes[currentRouteIndex] -= 1
        
    main(oled, draw)
    
    return "bus"


def center(oled, draw): 
    refreshIndexes()
    main(oled, draw)
    return "bus"


def back(oled, draw):
    
    return "apps"


def takeStartTime(elem):
        timeArray = elem.split("-")[1].split(":")
        return int(timeArray[0])*60+int(timeArray[1])


def getData():
    global lines
    global schedules
    global data
    global routes
    global currentIndexes
    global detailedForwardRoutes
    global detailedBackwardRoutes
    global detailedRoutes

    registeringData = False
    registeringRoutes = False
    for line in lines:
        if line == "Data:":
            registeringData = True
        if line == "Routes:":
            registeringData = False
            registeringRoutes = True
        if registeringData:
            data.append(line)
        elif registeringRoutes:
            routes.append(line)
        else:
            schedules.append(line)

    routes.pop(0)
    data.pop(0)
    schedules.pop(0)

    newSchedules = []
    currentSchedule = []
    for line in schedules:
        if line[1] == ".":
            newSchedules.append(currentSchedule)
            currentSchedule = []
        else:
            currentSchedule.append([line.partition("-")[0], line.partition("-")[2]])

    schedules = newSchedules

    newData = []
    currentData = []
    for line in data:
        if line[1] == ".":
            if currentData != []:
                newData.append(currentData)
                currentData = []
        else:
            currentData.append([line.partition("-")[0], line.partition("-")[2]])

    data = newData

    for idx, route in enumerate(routes):
        routes[idx] = [route.partition(":")[0], route.partition(":")[2]]

    detailedForwardRoutes = []

    route = routes[0]
    steps = route[1].split("-")
    for schedule in schedules[int(steps[0])-1]:
        duration = 0
        for group in data[int(steps[0])-1]:
            if group[0] == schedule[0]:
                duration = int(group[1])
        for time in schedule[1].split(","):
            timeArray = time.split(":")
            totalTime = int(timeArray[0])*60 + int(timeArray[1]) + duration + int(data[1][0][1]) + int(data[2][0][1])
            
            routeString = schedule[0]+"-"+time+"-"+'{:02d}:{:02d}'.format(*divmod(totalTime, 60))+"-"+str(duration + int(data[1][0][1]) + int(data[2][0][1]))
            detailedForwardRoutes.append(routeString)
    
    detailedRoutes.append(detailedForwardRoutes)
    
    detailedBackwardRoutes = []

    route = routes[1]
    steps = route[1].split("-")
    for schedule in schedules[int(steps[2])-1]:
        duration = 0
        pduration = int(data[2][0][1]) + int(data[1][0][1])
        for group in data[int(steps[2])-1]:
            if group[0] == schedule[0]:
                duration = int(group[1])
        for time in schedule[1].split(","):
            timeArray = time.split(":")
            startTime = int(timeArray[0])*60 + int(timeArray[1]) - pduration
            if startTime < 0:
                startTime = (int(timeArray[0])+24)*60 + int(timeArray[1]) - pduration
            endTime = startTime + pduration + duration
            routeString = schedule[0]+"-"+'{:02d}:{:02d}'.format(*divmod(startTime, 60))+"-"+'{:02d}:{:02d}'.format(*divmod(endTime, 60))+"-"+str(pduration+duration)
            detailedBackwardRoutes.append(routeString)
    
    detailedRoutes.append(detailedBackwardRoutes)

    detailedForwardRoutes.sort(key=takeStartTime)
    detailedBackwardRoutes.sort(key=takeStartTime)

    now = datetime.datetime.now()
    currentMinutes = now.hour*60+now.minute

    for idx, route in enumerate(detailedForwardRoutes):
        routeTimeArray = route.split("-")[1].split(":")
        if int(routeTimeArray[0])*60 + int(routeTimeArray[1]) > currentMinutes:
            currentIndexes[0] = idx
            break
        
    for idx, route in enumerate(detailedBackwardRoutes):
        routeTimeArray = route.split("-")[1].split(":")
        if int(routeTimeArray[0])*60 + int(routeTimeArray[1]) > currentMinutes:
            currentIndexes[1] = idx
            break


def refreshIndexes():
    global currentIndexes
    global detailedForwardRoutes
    global detailedBackwardRoutes
    
    now = datetime.datetime.now()
    currentMinutes = now.hour*60+now.minute

    for idx, route in enumerate(detailedForwardRoutes):
        routeTimeArray = route.split("-")[1].split(":")
        if int(routeTimeArray[0])*60 + int(routeTimeArray[1]) > currentMinutes:
            currentIndexes[0] = idx
            break
        
    for idx, route in enumerate(detailedBackwardRoutes):
        routeTimeArray = route.split("-")[1].split(":")
        if int(routeTimeArray[0])*60 + int(routeTimeArray[1]) > currentMinutes:
            currentIndexes[1] = idx
            break

getData()