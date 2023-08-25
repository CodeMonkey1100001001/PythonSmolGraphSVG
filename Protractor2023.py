import PythonSmolGraphSVG
import math

personHeight = 5
# for alpha in range(1,181):
#     halfAlpha = alpha / 2
#     b = personHeight / math.tan(halfAlpha * (3.14159265359 / 180))
#     print(halfAlpha, personHeight, b)



def drawGrid():
    global theDoc
    x = sg.minValueX
    # print("x minValueX", x, sg.minValueX)
    # print("sg.minValueY", sg.minValueY, sg.maxValueY)
    while x < sg.maxValueX:
        # print("x",x)
        theDoc += sg.graphLine(x, sg.minValueY, x, sg.maxValueY, 0.05, "#5f9b9c")
        x = x + 1.0

    y = sg.minValueY
    while y < sg.maxValueY:
        theDoc += sg.graphLine(sg.minValueX, y, sg.maxValueX, y, 0.05, "#5f9b9c")
        y = y + 1.0

    theDoc += sg.graphLine(sg.minValueX, 0, sg.maxValueX, 0, 0.1, "red")
    theDoc += sg.graphLine(0, sg.minValueY, 0, sg.maxValueY, 0.1, "green")


print("hello")

sg = PythonSmolGraphSVG.SmolGraph2SVG("mm")

sg.setSize(200, 200)
theDoc = sg.svgHeader()
# drawGrid()

# cartX, cartY = sg.polarToCartesian(0,0,100,90)
# theDoc += sg.graphLine(0,0,1.0,1.0,0.1,"green")
# theDoc += sg.graphLine(0,0,1.0,0.0,0.1,"blue")
#
# cartX, cartY = sg.polarToCartesian(0,0,100,180)
# theDoc += sg.graphLine(0,0,cartX,cartY,2.0,"blue")

subDivisions = 360/16
minorRadius = 1
majorRadius = 2

subSteps = 7

degreesBetween = (360 / subDivisions) - 7

lineWidth = 0.5
lineColor = "black"

tickLarge = 4
tickMedium = 3
tickSmall = 2

markLineWidth = 0.15

# first ticks
markingDiameter = 45.5 + 2.75
for i in range(0, 180):
    textWidth = len(str(i)) * 0.45
    tickText = 180 - i
    if tickText < 1:
        tickText = abs(tickText)
    if tickText == 90:
        textWidth = 1.2
    if tickText >99:
        textWidth = +1.5

    tickSize = tickSmall
    if not i % 5:
        tickSize = tickMedium
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i + textWidth, markingDiameter - 4.25, "4pt", "#000000", flip=True)
    if not i % 10:
        tickSize = tickLarge
    theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, i, markingDiameter, i, markLineWidth, "#000000")

# second ticks
# 2nd persons height
markingDiameter = 55.5 + 2.75
personHeight = 5 + (.5/12)
# for distance in range(1,11):
#     theDegrees = 90 - (math.atan(personHeight/distance)*(180/3.14159265359))
#     print("personHeight",personHeight,"theDistance",distance,"angle",theDegrees)
#     theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, theDegrees, markingDiameter, theDegrees, markLineWidth, "#000000")
#     theDoc += sg.graphPolarText(str(distance), 0, 0, theDegrees+0.6, markingDiameter - 2.2, "6pt", "#000000", flip=True)

for distance in [1,2,3,4,5,6,7,8,9,10,12,14,18,24,34,55]:
    degOffset = 0.65
    if (distance>9):
        degOffset = 1.4
    theDegrees = 90 - (math.atan(personHeight/distance)*(180/3.14159265359))
    print("personHeight",personHeight,"theDistance",distance,"angle",theDegrees)
    theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, theDegrees, markingDiameter, theDegrees, markLineWidth, "#000000")
    theDoc += sg.graphPolarText(str(distance), 0, 0, theDegrees + degOffset, markingDiameter - 2.2, "6pt", "#000000", flip=True)

evenOdd = 0
for distance in [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-12,-14,-18,-24,-34,-55]:
    degOffset = 2.1
    if distance < -9:
        degOffset = 3.0
    theDegrees = 90 - (math.atan(distance / personHeight)*(180/3.14159265359))
    print("personHeight",personHeight,"theDistance",distance,"angle",theDegrees)
    distanceText = abs(distance)
    theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, theDegrees, markingDiameter, theDegrees, markLineWidth, "#000000")
    theDoc += sg.graphPolarText(str(distanceText), 0, 0, theDegrees + degOffset, markingDiameter - 2.2 + (evenOdd * 1.5), "5.5pt", "#000000", flip=True)
    if evenOdd == 1:
        evenOdd = 0
    else:
        evenOdd = 1

# markingDiameter = 55.5 + 2.75
# for i in range(0, 180):
#     tickSize = tickSmall
#     if not i % 5:
#         tickSize = tickMedium
#     if not i % 10:
#         tickSize = tickLarge
#     theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, i, markingDiameter, i, markLineWidth, "#000000")

tickLarge = 4.25
tickMedium = 3.25
tickSmall = 2.25

# third ticks degrees 90 to 0 to 90
markingDiameter = 65.5 + 2.75 -0.25
for i in range(0, 181):
    textWidth = len(str(i)) * 0.55
    tickText = 90 - i
    if tickText < 1:
        tickText = abs(tickText)
    if tickText == 90:
        textWidth = 2.5
        if i > 90:
            textWidth = -0.5

    tickSize = tickSmall
    if not i % 5:
        tickSize = tickMedium
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i + textWidth, 64.5 - 0.25, "6pt", "#000000", flip=True)
    if not i % 10:
        tickSize = tickLarge
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i + textWidth, 64.5-0.25, "6pt", "#000000", flip=True)
        # theDoc += sg.graphDiskText(0,40,i, "#00ff00",str(i))
    theDoc += sg.graphDualPolarLine(0, 0, markingDiameter-tickSize, i, markingDiameter, i, markLineWidth, "#000000")

# i = 0
# while i < 90:
#     theDoc += sg.graphDualPolarLine(0,0, minorRadius,   i               , majorRadius,  i,                 lineWidth, lineColor)
#     theDoc += sg.graphDualPolarLine(0,0, minorRadius,   i + degreesBetween, majorRadius,  i + degreesBetween,  lineWidth, lineColor)
#     theDoc += sg.graphArc(0, 0, majorRadius, i, i + degreesBetween, lineWidth, lineColor)
#
#     subNum = minorRadius
#     while subNum < majorRadius:
#         theDoc += sg.graphArc(0,0,subNum,i,i + degreesBetween, lineWidth, lineColor)
#         subNum = subNum + ( (majorRadius-minorRadius) / subSteps )
#         #theX , theY = sg.polarToCartesianFlip(0,0,subNum-0.18,i+2)
#         #theDoc += sg.graphText("0",theX,theY,"#000000",24)
#     i = i + (360/subDivisions)

theDoc += sg.graphCircle(0, 0, 4.25 , 0.5, "red")
# theDoc += sg.graphCircle(0, 0, minorRadius * 0.85 , lineWidth, "red")
# theDoc += sg.graphPolarLine(-2.0,0,71,0,1,"#ff0000")
theDoc += sg.graphDualPolarLine(0, 0, 0, 0, 68, 0, 0.5, "#ff0000")
theDoc += sg.graphDualPolarLine(0, 0, 0, 180, 68, 180, 0.5, "#ff0000")
theDoc += sg.drawArc(0, 0, 67.5, -0.4, 180+0.4, 0.5, "#ff0000")


if False:
    theX, theY = sg.polarToCartesianFlip(0,0,3,45)
    theDoc += sg.graphText("45deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,90)
    theDoc += sg.graphText("90deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,225)
    theDoc += sg.graphText("225deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,135)
    theDoc += sg.graphText("135deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,315)
    theDoc += sg.graphText("315deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,0)
    theDoc += sg.graphText("0deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesianFlip(0,0,3,180)
    theDoc += sg.graphText("180deg",theX,theY,"#000000","24pt")

    theX, theY = sg.polarToCartesian(0,0,3,180-270)
    theDoc += sg.graphText("270deg",theX,theY,"#000000","24pt")

theDoc += sg.svgFooter()

fp = open("/tmp/misc/test.svg","w")
fp.writelines(theDoc)
fp.close()

#print(theDoc)
