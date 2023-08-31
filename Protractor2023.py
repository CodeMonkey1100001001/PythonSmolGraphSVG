from pprint import pprint

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

sg = PythonSmolGraphSVG.SmolGraph2SVG("cm")

sg.setSize(20, 20, -10, 10, -10, 10)
theDoc = sg.svgHeader()
drawGrid()

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

# in cm
tickLarge = .5
tickMedium = .4
tickSmall = .3

markLineWidth = 0.05 # 0.5mm fine line

# first ticks
markingRadius = 8
for i in range(0, 360):
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
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i + textWidth, markingRadius + 0.25 , "8pt", "#000000", flip=True)
    if not i % 10:
        tickSize = tickLarge
    theDoc += sg.graphDualPolarLine(0, 0, markingRadius-tickSize, i, markingRadius, i, markLineWidth, "#000000")

theDoc += sg.graphLine(-9,-9,9,9,0.1,"#0000cc")
theDoc += sg.graphCircle(0,0,9,0.2,"#ffcccc")

# line on circle

print("XGrid")
for x in range(0,5):
    theReturn = sg.circle_line_segment_intersection([0,0],5,[x, 0],[x,5],full_line=False)
    pprint(theReturn)
    #print("theReturn",theReturn,type(theReturn))
    # if (len(theReturn)>1):
    #     (x, y) = theReturn[0]
    #     (h, v) = theReturn[1]
    #     print(x,y,h,v)
    #     theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")
    y = 0
    (h, v) = theReturn[0]
    theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")

print("YGrid")
for y in range(0,5):
    theReturn = sg.circle_line_segment_intersection([ 0, 0], 5, [0, y], [5, y], full_line=False)
    pprint(theReturn)
    #print("theReturn",theReturn,type(theReturn))
    # if (len(theReturn)>1):
    #     (x, y) = theReturn[0]
    #     (h, v) = theReturn[1]
    #     print(x,y,h,v)
    #     theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")
    x = 0
    (h, v) = theReturn[0]
    theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")


theDoc += sg.svgFooter()



fp = open("/tmp/misc/test.svg","w")
fp.writelines(theDoc)
fp.close()

#print(theDoc)
