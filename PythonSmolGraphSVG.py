# PythonSmolGraphSVG.py
# very simple python to basic plain SVG generator
# useful for making parametric graphs for inkscape.
# Version 20230908.2001
# SVG is normally 0,0 at upper left corner this lib
# is set to use 0,0 and a normal cartesian grid with +x,+y in
# the upper right quadrant and -x,-y in the lower left.

import math

from random import random


class SmolGraph2SVG:
    def __init__(self, units):

        self.dpi = 96
        self.penWidth = 0.19685  # 0.5mm pen
        self.fontSize = "10pt"
        self.color = "#000000"
        self.fontFamily = "monospace"

        if units == "inch":
            self.dpi = 96
        if units == "mm":
            self.dpi = 96/2.54/10
            self.penWidth = 0.5  # 0.5mm pen
        if units == "cm":
            self.dpi = 96/2.54
            self.penWidth = 0.05  # 0.5mm pen
        if units == "px":
            self.dpi = 1

        self.document = ""

        self.physicalWidth = 10 * self.dpi
        self.physicalHeight = 10 * self.dpi

        self.minValueX = -5  # in inches
        self.maxValueX = 5  # in inches

        self.minValueY = -5  # in inches
        self.maxValueY = 5  # in inches

        # this allows multiple graphs to live on the same screen/print  - untested
        self.startX = 0  # where on the Physical screen to start
        self.startY = 0  # where on the physical screen to start

        # this is so that the cartesian center can be offset
        self.cartCenterX = 0  # -1 * (self.physicalWidth / 2)
        self.cartCenterY = 0  # -1 * (self.physicalHeight / 2)

    def setSize(self, physicalWidth, physicalHeight, minX, maxX, minY, maxY):
        self.physicalWidth = physicalWidth * self.dpi
        self.physicalHeight = physicalHeight * self.dpi
        self.minValueX = minX
        self.maxValueX = maxX
        self.minValueY = minY
        self.maxValueY = maxY

    def getSizeHuman(self):
        retV = f'''
PythonSmolGraphSVG Sizes
dpi={self.dpi}
physicalWidth={self.physicalWidth}
physicalHeight={self.physicalHeight}
minValueX = {self.minValueX}
maxValueX = {self.maxValueX}
minValueY = {self.minValueY}
maxValueY = {self.maxValueY}
cartCenterX = {self.cartCenterX}
cartCenterY = {self.cartCenterY}

'''
        # cartCenterX = {self.cartCenterX}
        # cartCenterY = {self.cartCenterY}
        return retV

#
#         self.startX = 0  # where on the Physical screen to start
#         self.startY = 0  # where on the physical screen to start
#
#         #self.widthX = self.physicalWidth
#         #self.heightY = self.physicalHeight
#
#         self.cartCenterX = 0  # -1 * (self.physicalWidth / 2)
#         self.cartCenterY = 0  # -1 * (self.physicalHeight / 2)

    def setCenter(self, x, y):
        self.cartCenterX = x * self.dpi  # -1 * (self.physicalWidth / 2)
        self.cartCenterY = y * self.dpi  # -1 * (self.physicalHeight / 2)

    def svgHeader(self,extraData=""):
        SVGDOCUMENT = ""
        GRAPHWIDTH = self.physicalWidth
        GRAPHHEIGHT = self.physicalHeight
        # SVGDOCUMENT += "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"" + str(GRAPHWIDTH) + "\"  height=\"" + str(GRAPHHEIGHT) + "\"  >\n"
        SVGDOCUMENT += f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
            width="{str(GRAPHWIDTH)}" height="{str(GRAPHHEIGHT)}"  
            xmlns:xlink="http://www.w3.org/1999/xlink"
            {extraData}
            >\n'''
        # SVGDOCUMENT += "<rect x=\"0\" y=\"0\" width=\"" + str(GRAPHWIDTH) + "\" height=\"" + str(GRAPHHEIGHT) +"\"  style=\"fill:white; stroke-width:3;stroke:rgb(0,0,0)\"/>\n"
        # print("[$SVGDOCUMENT]\n")
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def svgFooter(self):
        SVGDOCUMENT = "</svg>\n"
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    # noinspection PyMethodMayBeStatic
    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}')
        fromRange = fromHigh - fromLow
        toRange = toHigh - toLow
        scaleFactor = toRange / fromRange
        tmpValue = value - fromLow
        tmpValue *= scaleFactor
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}, returnValue={tmpValue} toLow={toLow}')
        return tmpValue + toLow

    # noinspection PyMethodMayBeStatic
    # def polarToCartesian(self, centerX, centerY, radius, angleInDegrees):
    #     angleInRadians = (angleInDegrees-90) * math.pi / 180.0
    #     x = centerX + (radius * math.cos(angleInRadians))
    #     y = centerY + (radius * math.sin(angleInRadians))
    #     return x, y

    # def polarToCartesianScaled(self, centerX, centerY, radius, angleInDegrees):
    #     radius = radius * self.dpi
    #     centerX = self.map(centerX, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
    #     centerY = self.map(centerY, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
    #     angleInRadians = (angleInDegrees-90) * math.pi / 180.0
    #     x = centerX + (radius * math.cos(angleInRadians))
    #     y = centerY + (radius * math.sin(angleInRadians))
    #     return x, y

    # Cartesian to Polar and Polar to Cartesian
    # I expect a cartesian grid where -X is left +X is right
    # -Y is down and +Y is up
    # 5,5 is in Quadrant I (Quadrant #1)
    # -5, -5 is in Quadrant III (Quadrant #3)
    # Quadrants are numbered counter clockwise
    # 0 degrees is X=0 and Y>0 (North)
    # 90 degrees is Y=0 and X>0 (East)
    # 180 degrees is X=0 and Y<0 (South)
    # 270 degrees is Y=0 and X<0 (West)
    # 45 degrees is X>0 and  X = Y (North East)
    def cartesianToPolar(self, x, y):
        # this function needs the ability to have a x,y offset
        theRadians = math.atan2(x, y)
        # theDegrees = math.degrees(theRadians)
        # theDegrees = (180 / 3.14159265359) * theRadians
        theDegrees = (180 / math.pi) * theRadians
        if (theDegrees < 0):
            theDegrees = 360 + theDegrees
        theRadius = math.sqrt((x * x) + (y * y))
        return theDegrees, theRadius

    # Polar to Cartesian formula.
    def polarToCartesian(self, centerX, centerY, radius, angleInDegrees):
        # angleInDegrees = angleInDegrees - 90
        angleInRadians = math.radians(angleInDegrees)

        # angleInRadians = angleInDegrees  * 3.14159265359 / 180.0 # manual method
        # when flipped the cos and sin here are flipped because the SVG starts in upper left # not true
        x = centerX + (radius * math.sin(angleInRadians))  # would normally be sin
        y = centerY + (radius * math.cos(angleInRadians))  # would normally be cos

        return x, y

    # Polar to Cartesian formula. Flipped
    # this is used internally to flip the Y
    def polarToCartesianFlip(self, centerX, centerY, radius, angleInDegrees):
        angleInDegrees = angleInDegrees - 90
        angleInRadians = math.radians(angleInDegrees)

        # angleInRadians = angleInDegrees  * 3.14159265359 / 180.0 # manual method
        # the cos and sin here are flipped because the SVG starts in upper left
        x = centerX + (radius * math.cos(angleInRadians))  # would normally be sin
        y = centerY + (radius * math.sin(angleInRadians))  # would normally be cos

        return x, y

    # use user supplied or default
    def getWidth(self, width):
        if (width is False):
            width = self.penWidth * self.dpi
        else:
            width = width * self.dpi
        return width

    # use user supplied or default
    def getColor(self, color):
        if (color is False):
            color = self.color
        return color

    def getFontSize(self, fontSize):
        if (fontSize is False):
            fontSize = self.fontSize
        return fontSize

    def graphLine(self, x, y, h, v, width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        # width = width * self.dpi
        # the mapping takes care of the dpi no more x1 = x1 * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + self.cartCenterX
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + self.cartCenterX
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        # x1 = x1 * self.dpi         #x2 = x2 * self.dpi         #y1 = y1 * self.dpi         #y2 = y2 * self.dpi
        SVGDOCUMENT = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        # print("x",x,"x1",x1)
        # print("x",x,"x2",x2)
        # print("x",x,"y1",y1)
        # print("x",x,"y2",y2)

        return SVGDOCUMENT

    def graphRectangle(self, x, y, h, v, width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        SVGDOCUMENT += f'<polygon points="{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}" style="fill: none; stroke:{color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphRectangleFilled(self, x, y, h, v, fillColor=False,  strokeWidth=False, strokeColor=False):
        strokeWidth = self.getWidth(strokeWidth)
        strokeColor = self.getColor(strokeColor)
        fillColor = self.getColor(fillColor)
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        SVGDOCUMENT += f'<polygon points="{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}" style="fill: {fillColor}; stroke:{strokeColor}; stroke-width: {strokeWidth};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphCircle(self, x, y, radius, width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: none; stroke: {color}; stroke-width: {width}"  />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDisk(self, x, y, radius, color=False):
        color = self.getColor(color)
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: {color}; stroke: none;"  />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDiskText(self, x, y, radius, textValue, color=False):
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: {color}; stroke: none;"  ><title>{textValue}</title></circle>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphText(self, textValue, x, y, size=False, color=False,  textAnchor="start"):
        size = self.getFontSize(size)
        color = self.getColor(color)
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        # y1=y1+(size/3)
        # print("text",x1,y1)
        SVGDOCUMENT += f'<text x="{x1}" y="{y1}" fill="{color}" font-family="{self.fontFamily}" font-size="{size}" text-anchor="{textAnchor}">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphTextRotate(self, textValue, x, y, degrees, color=False, textAnchor="start"):
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + self.cartCenterX
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY) - self.cartCenterY
        # y1=y1+(size/3)
        SVGDOCUMENT += f'<text x="{x1}" y="{y1}" fill="{color}" font-family="{self.fontFamily}" font-size="{self.fontSize}"  transform="rotate({degrees} {x1},{y1})" text-anchor="{textAnchor}">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDualPolarLine(self, x, y, radius1, startAngle1, radius2, startAngle2, width=False, color=False):
        makeRandom = False
        width = self.getWidth(width)
        color = self.getColor(color)
        # x = x * self.dpi
        # y = y * self.dpi
        radius1 = radius1 * self.dpi
        radius2 = radius2 * self.dpi

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        startX, startY = self.polarToCartesianFlip(x, y, radius2, startAngle2)
        endX, endY = self.polarToCartesianFlip(x, y, radius1, startAngle1)

        if makeRandom is True:
            scaleFactor = 1.0
            startX = startX + random() * scaleFactor
            startY = startY + random() * scaleFactor
            endX = endX + random() * scaleFactor
            endY = endY + random() * scaleFactor

        SVGDOCUMENT = f'<line x1="{startX}" y1="{startY}" x2="{endX}" y2="{endY}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphPolarLine(self, x, y, radius, startAngle,  width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        # x = x * self.dpi
        # y = y * self.dpi
        radius = radius * self.dpi
        # width = float(width) * self.dpi * 1.0
        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        # startX, startY = self.polarToCartesian(x, y, radius, endAngle)
        endX, endY = self.polarToCartesianFlip(x, y, radius, startAngle)
        SVGDOCUMENT = f'<line x1="{x}" y1="{y}" x2="{endX}" y2="{endY}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    # def drawArc(self, x, y, radius, startAngle, endAngle, width, color):
    #     #x = x * self.dpi
    #     #y = y * self.dpi
    #     radius = radius * self.dpi
    #     # print("width", width,"dpi", self.dpi)
    #     strokeWidth = float(width) * float(self.dpi) * 1.0
    #
    #     # x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
    #     # y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
    #     x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
    #     y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
    #
    #     startX, startY = self.polarToCartesianFlip(x, y, radius, endAngle)
    #     endX, endY = self.polarToCartesianFlip(x, y, radius, startAngle)
    #     if (endAngle - startAngle <= 180):
    #         largeArcFlag = 0
    #     else:
    #         largeArcFlag = 1
    #     # largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
    #     # <path id="arc1" fill="none" stroke="#446688" stroke-width="2" d="M 40 20 A 20 20 0 0 0 34.14213562373095 5.857864376269051" onclick="doit();"></path>
    #     SVGDOCUMENT = f'<path fill="none" stroke="{color}" stroke-width="{strokeWidth}" '
    #     # "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
    #     SVGDOCUMENT += f'd="M {startX} {startY} A {radius}, {radius}, 0, {largeArcFlag}, 0,  {endX}, {endY}"'
    #     SVGDOCUMENT += "></path>\n"
    #
    #     self.document += SVGDOCUMENT
    #     return SVGDOCUMENT

    def graphArc(self, x, y, radius, startAngle, endAngle, width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        radius = radius * self.dpi

        sweepFlag = "0"

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        startX, startY = self.polarToCartesianFlip(x, y, radius, endAngle)
        endX, endY = self.polarToCartesianFlip(x, y, radius, startAngle)

        if (endAngle - startAngle <= 180):
            largeArcFlag = 0
        else:
            largeArcFlag = 1
        # largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
        # <path id="arc1" fill="none" stroke="#446688" stroke-width="2" d="M 40 20 A 20 20 0 0 0 34.14213562373095 5.857864376269051" onclick="doit();"></path>
        SVGDOCUMENT = f'<path fill="none" stroke="{color}" stroke-width="{width}" '
        # "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
        SVGDOCUMENT += f'd="M {startX} {startY} A {radius}, {radius}, 0, {largeArcFlag}, {sweepFlag},  {endX}, {endY}"'
        SVGDOCUMENT += "></path>\n"

        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def output(self):
        return self.document

    def graphPolarText(self, textValue, x, y, degrees, radius, size=False, color=False, flip=False, textAnchor="start"):
        size = self.getFontSize(size)
        color = self.getColor(color)
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        degrees = degrees
        # print(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY, self.cartCenterY)
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        polarX, polarY = self.polarToCartesianFlip(x1, y1, radius, degrees)
        x1 = polarX
        y1 = polarY
        if flip is True:
            degrees = degrees + 180
        # text anchor
        # textAnchor = "start"
        # textAnchor = "middle"
        # textAnchor = "end"
        # SVGDOCUMENT += f'<text x="{x1}" y="{y1}" transform="rotate({degrees} {x1},{y1})" fill="{color}" font-face="sans" font-size="{size}">{textValue}</text>\n'
        SVGDOCUMENT += f'<text nox="{x1}" noy="{y1}" transform="translate( {x1},{y1}) rotate({degrees}) " fill="{color}" font-family="{self.fontFamily}" font-size="{size}" text-anchor="{textAnchor}">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    # mostly working kinda breaks the standard
    def graphPolygon(self, thePoints, width=False, color=False):
        width = self.getWidth(width)
        color = self.getColor(color)
        SVGDOCUMENT = ""

        print("graphing a polygon", thePoints)
        SVGDOCUMENT += f'<polygon points="'
        for oneSet in thePoints:
            print("one", oneSet, oneSet[0], oneSet[1])
            x = oneSet[0]
            y = oneSet[1]
            x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth) + (self.cartCenterX)
            y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
            SVGDOCUMENT += f'{x1},{y1} '

        SVGDOCUMENT += f'" style="fill: none; stroke:{color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphImage(self, filename, x, y, width, height, rotation, center=True, extraTransform=""):
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        # w1 = self.map(width, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)
        # h1 = self.map(height, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)
        w1 = width * self.dpi
        h1 = height * self.dpi
        rx = x1
        ry = y1

        if center is True:
            x1 = x1 - (w1/2)
            y1 = y1 - (h1/2)
        SVGDOCUMENT = ""
        # SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" href="{filename}"/>\n'
        SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" xlink:href="{filename}" transform="rotate({rotation},{rx},{ry}) {extraTransform}"  opacity="0.3"/>\n'
        #
        # SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" href="{filename}" transform="rotate({rotation},{rx},{ry})"/>\n'

        return SVGDOCUMENT

    def mmtoinches(self, unitInMM):
        inches = unitInMM / 25.4
        return inches

    def graphImageInclude(self, filename, x, y, width, height, rotation, center=True, extraTransform=""):
            x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (
                self.cartCenterX)
            y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight,
                          self.startY) - self.cartCenterY
            # w1 = self.map(width, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)
            # h1 = self.map(height, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)
            w1 = width * self.dpi
            h1 = height * self.dpi
            rx = x1
            ry = y1

            if center is True:
                x1 = x1 - (w1 / 2)
                y1 = y1 - (h1 / 2)

            file_path = "/tmp/misc/" + filename
            file_contents=""
            with open(file_path, 'r') as file:
                file_contents = file.read()
            SVGDOCUMENT = ""
            centerFontX = x1 #- width/2 * -1.0
            centerFontY = y1 #- height/2 * -1.0
            # SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" href="{filename}"/>\n'
            #SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" xlink:href="{filename}" transform="rotate({rotation},{rx},{ry}) {extraTransform}" />\n'
            SVGDOCUMENT += f'''<g transform="rotate({rotation},{rx},{ry}) translate({centerFontX},{centerFontY}) scale({width},{height}) " >
            {file_contents}
            </g>'''

            #
            # SVGDOCUMENT += f'<image x="{x1}" y="{y1}" width="{w1}" height="{h1}" href="{filename}" transform="rotate({rotation},{rx},{ry})"/>\n'

            return SVGDOCUMENT

