# from pprint import pprint

import PythonSmolGraphSVG
import PythonSmolGraphFancyStuff


# import math

def drawGrid():
    global theDoc
    dgx = sg.minValueX
    # print("x minValueX", x, sg.minValueX)
    # print("sg.minValueY", sg.minValueY, sg.maxValueY)
    while dgx < sg.maxValueX:
        # print("dgx",dgx)
        theDoc += sg.graphLine(dgx, sg.minValueY, dgx, sg.maxValueY, 0.025, "#5f9b9c")
        dgx = dgx + 1.0

    dgy = sg.minValueY
    while dgy < sg.maxValueY:
        theDoc += sg.graphLine(sg.minValueX, dgy, sg.maxValueX, dgy, 0.025, "#5f9b9c")
        dgy = dgy + 1.0

    theDoc += sg.graphLine(sg.minValueX, 0, sg.maxValueX, 0, 0.1, "red")
    theDoc += sg.graphLine(0, sg.minValueY, 0, sg.maxValueY, 0.1, "green")


print("hello")

sg = PythonSmolGraphSVG.SmolGraph2SVG("cm")
sgf = PythonSmolGraphFancyStuff.SmolGraphFancy("cm")

sg.setSize(20, 20, -10, 10, -10, 10)
# sg.setCenter(-10,-10)

theDoc = sg.svgHeader()
drawGrid()

# cartX, cartY = sg.polarToCartesian(0,0,100,90)
# theDoc += sg.graphLine(0,0,1.0,1.0,0.1,"green")
# theDoc += sg.graphLine(0,0,1.0,0.0,0.1,"blue")
#
# cartX, cartY = sg.polarToCartesian(0,0,100,180)
# theDoc += sg.graphLine(0,0,cartX,cartY,2.0,"blue")

theDoc += sg.graphLine(-8, 8, 8, -8, 0.05, "#ffcccc")
theDoc += sg.graphLine(-8, -8, 8, 8, 0.05, "#ccccff")

subDivisions = 360 / 16
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

markLineWidth = 0.05  # 0.5mm fine line

# first ticks
markingRadius = 8
for i in range(0, 360):
    textWidth = len(str(i)) * 0.45
    tickText = i
    if tickText < 1:
        tickText = abs(tickText)
    if tickText == 90:
        textWidth = 1.2
    if tickText > 99:
        textWidth = +1.5

    tickSize = tickSmall
    if not i % 5:
        tickSize = tickMedium
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i, markingRadius + 0.75, "8pt", "#000000",
                                    flip=False)
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i, markingRadius + -0.5, "8pt", "#000000",
                                flip=False,textAnchor="middle")
        theDoc += sg.graphPolarText(str(tickText), 0, 0, i, markingRadius + -0.75, "8pt", "#000000",
                                flip=False, textAnchor="end")
    if not i % 10:
        tickSize = tickLarge
    theDoc += sg.graphDualPolarLine(0, 0, markingRadius + tickSize, i, markingRadius, i, markLineWidth, "#000000")

theDoc += sg.graphCircle(0, 0, markingRadius, markLineWidth, "#000000")
theDoc += sg.graphCircle(0, 0, markingRadius + 1.0, markLineWidth, "#000000")

# line on circle

print("XGrid")
for x in range(0, 8):
    theReturn = sgf.circle_line_segment_intersection([0, 0], markingRadius, [x, 0], [x, 8], full_line=False)
    # pprint(theReturn)
    # print("theReturn",theReturn,type(theReturn))
    # if (len(theReturn)>1):
    #     (x, y) = theReturn[0]
    #     (h, v) = theReturn[1]
    #     print(x,y,h,v)
    #     theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")
    y = 0
    (h, v) = theReturn[0]
    theDoc += sg.graphLine(x, y, h, v, markLineWidth, "#0000ff")

print("YGrid")
for y in range(0, 8):
    theReturn = sgf.circle_line_segment_intersection([0, 0], markingRadius, [0, y], [8, y], full_line=False)
    # pprint(theReturn)
    # print("theReturn",theReturn,type(theReturn))
    # if (len(theReturn)>1):
    #     (x, y) = theReturn[0]
    #     (h, v) = theReturn[1]
    #     print(x,y,h,v)
    #     theDoc += sg.graphLine(x, y, h, v, 0.2, "#0000ff")
    x = 0
    (h, v) = theReturn[0]
    theDoc += sg.graphLine(x, y, h, v, markLineWidth, "#0000ff")

# make sure PolarToCartesian and CartesianToPolar algos work
print("=======================================")
print("Testing Polar to Cart and Cart to Polar")
theDoc += sg.graphLine(-4, 2, 4, -4, 0.3, color="#cc44cc")
theDoc += sg.graphPolarText("XiX", 0, 0, 45, 5.5, "12pt", "#ff0000", textAnchor="middle")
theDoc += sg.graphPolarLine(0, 0, 5, 45, 0.2, "#00ff00")

newDeg, newRadius = sg.cartesianToPolar(-9, -3)
print("newDeg", newDeg, "newRadius", newRadius)
newX, newY = sg.polarToCartesian(0, 0, newRadius, newDeg)
print("newX", newX, "newY", newY)

theDoc += sg.graphLine(0, 0, newX, newY, 0.3, "#FA0000")
theDoc += sg.graphPolarLine(0, 0, newRadius, newDeg, 0.1, "#FAF700")

print("should see a red line with a smaller yellow line in it")

print("==================")
print("normal test begins")

theDoc += sg.graphArc(0, 0, 7, 45, 45 + 90, 0.2, "#FF00FF")
theDoc += sg.graphRectangle(-4, -4, -3, -3, 0.1, "#770737")
theDoc += sg.graphRectangleFilled(-4, -5, -3, -4, "#F33A6A", 0.1, "#0000cc")
theDoc += sg.graphCircle(-5, 5, 1.0, 0.2, "#0000ff")
theDoc += sg.graphDisk(-5, 3, 1.0, "#00ccff")
theDoc += sg.graphDiskText(-5, 1, 1.0, "disk text", "#0000cc")  # graph a disc but with hover help
theDoc += sg.graphText("PlainText", 1, -5, "24pt", "#cc0000")
theDoc += sg.graphTextRotate("Rotated66", 4, -5, "12pt", 66, "#cc00cc")
theDoc += sg.graphDualPolarLine(0, 0, 2.5, 66, 3.0, 67, 0.1, "#ff4444")
theDoc += sg.graphPolarLine(0, 0, 9.5, 12, 0.1, "#cc4433")
# theDoc += sg.drawArc(4,-4,2,45,45+90,0.1,"#fafa00")
theDoc += sg.graphArc(4.5, -4.5, 2, 45, 45 + 90, 0.1, "#fafa00")
theDoc += sg.graphLine(-5, -9, 5, -9)  # test using defaults for width and color


# vernier for compass
for i in range(0,11):
    theDoc += sg.graphDualPolarLine(0,0,7.5,i - (0.1 * i) ,8,i - (0.1 * i),width=0.05)
    theDoc += sg.graphPolarText(str(i),0,0,i,7.25,size="4pt", textAnchor="middle")

# test font-family change
sg.fontFamily = "sans"
theDoc += sg.graphText("PlainSansText", 1.5, -6, "24pt", "#cc0000")
theDoc += sg.svgFooter()

fp = open("/tmp/misc/test.svg", "w")
fp.writelines(theDoc)
fp.close()

# print(theDoc)

print(sg.getSizeHuman())
