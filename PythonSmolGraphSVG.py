# PythonSmolGraphSVG.py
# very simple python to basic plain SVG generator
# useful for making parametric graphs for inkscape.
# Version 20230828.0712
# SVG is normally 0,0 at upper left corner this lib
# is set to use 0,0 and a normal cartesian grid with +x,+y in
# the upper right quadrant and -x,-y in the lower left.

import math


class SmolGraph2SVG:
    def __init__(self, units):

        self.dpi = 96
        if units == "inch":
            self.dpi = 96
        if units == "mm":
            self.dpi = 96/2.54/10
        if units == "cm":
            self.dpi = 96/2.54
        if units == "px":
            self.dpi = 1

        self.document = ""

        self.physicalWidth = 10 * self.dpi
        self.physicalHeight = 10 * self.dpi

        self.minValueX = -5  # in inches
        self.maxValueX = 5  # in inches

        self.minValueY = -5  # in inches
        self.maxValueY = 5  # in inches

        self.startX = 0  # where on the Physical screen to start
        self.startY = 0  # where on the physical screen to start

    def setSize(self, physicalWidth, physicalHeight, minX, maxX, minY, maxY):
        self.physicalWidth = physicalWidth   * self.dpi
        self.physicalHeight = physicalHeight  * self.dpi
        self.minValueX = minX
        self.maxValueX = maxX
        self.minValueY = minY
        self.maxValueY = maxY

    def getSizeHuman(self):
        retV = f'''
Sizes\n
dpi={self.dpi}
physicalWidth={self.physicalWidth}
physicalHeight={self.physicalHeight}
minValueX = {self.minValueX}
maxValueX = {self.maxValueX}
minValueY = {self.minValueY}
maxValueY = {self.maxValueY}
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

    def svgHeader(self):
        SVGDOCUMENT = ""
        GRAPHWIDTH = self.physicalWidth
        GRAPHHEIGHT = self.physicalHeight
        SVGDOCUMENT += "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"" + str(GRAPHWIDTH) + "\"  height=\"" + str(GRAPHHEIGHT) + "\"  >\n"
        # SVGDOCUMENT += "<rect x=\"0\" y=\"0\" width=\"" + str(GRAPHWIDTH) + "\" height=\"" + str(GRAPHHEIGHT) +"\"  style=\"fill:white; stroke-width:3;stroke:rgb(0,0,0)\"/>\n"
        # print("[$SVGDOCUMENT]\n")
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def svgFooter(self):
        SVGDOCUMENT = "</svg>\n"
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}')
        fromRange = fromHigh - fromLow
        toRange = toHigh - toLow
        scaleFactor = toRange / fromRange
        tmpValue = value - fromLow
        tmpValue *= scaleFactor
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}, returnValue={tmpValue} toLow={toLow}')
        return tmpValue + toLow

    def polarToCartesianFlip(self, centerX, centerY, radius, angleInDegrees):
        angleInDegrees = 180 - angleInDegrees
        angleInRadians = (angleInDegrees-90) * math.pi / 180.0
        x = centerX + (radius * math.cos(angleInRadians))
        y = centerY + (radius * math.sin(angleInRadians))
        return x, y

    def polarToCartesian(self, centerX, centerY, radius, angleInDegrees):
        angleInRadians = (angleInDegrees-90) * math.pi / 180.0
        x = centerX + (radius * math.cos(angleInRadians))
        y = centerY + (radius * math.sin(angleInRadians))
        return x, y

    def polarToCartesianScaled(self, centerX, centerY, radius, angleInDegrees):
        radius = radius * self.dpi

        centerX = self.map(centerX, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # - self.cartCenterX
        centerY = self.map(centerY, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)  # + self.cartCenterY

        angleInRadians = (angleInDegrees-90) * math.pi / 180.0
        x = centerX + (radius * math.cos(angleInRadians))
        y = centerY + (radius * math.sin(angleInRadians))
        return x, y

    def cartesianToPolar(self, x, y):
        return False

    def graphLine(self, x, y, h, v, width, color):
        width = width * self.dpi
        # the mapping takes care of the dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -self.cartCenterX
        # print("x",x,"x1",x1)
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -self.cartCenterX
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        # x1 = x1 * self.dpi         #x2 = x2 * self.dpi         #y1 = y1 * self.dpi         #y2 = y2 * self.dpi
        SVGDOCUMENT = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        # print("x",x,"x1",x1)
        # print("x",x,"x2",x2)
        # print("x",x,"y1",y1)
        # print("x",x,"y2",y2)

        return SVGDOCUMENT

    def graphRectangle(self, x, y, h, v, width, color):
        SVGDOCUMENT = ""
        width = width * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        SVGDOCUMENT += f'<polygon points="{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}" style="fill: none; stroke:{color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphRectangleFilled(self, x, y, h, v, width, color, strokeWidth, strokeColor):
        SVGDOCUMENT = ""
        strokeWidth = width * self.dpi # ide complains that this var is not used.
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        x2 = self.map(h, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        y2 = self.map(v, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        SVGDOCUMENT += f'<polygon points="{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}" style="fill: {color}; stroke:{strokeColor}; stroke-width: {strokeWidth};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphCircle(self, x, y, radius, width, color):
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        width = width * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: none; stroke: {color}; stroke-width: {width}"  />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDisk(self, x, y, radius, color):
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: {color}; stroke: none;"  />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDiskText(self, x, y, radius, color, textValue):
        SVGDOCUMENT = ""
        radius = radius * self.dpi
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        SVGDOCUMENT += f'<circle cx="{x1}" cy="{y1}" r="{radius}" style="fill: {color}; stroke: none;"  ><title>{textValue}</title></circle>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphText(self, textValue, x, y, size, color):
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)  # +self.cartCenterY
        # y1=y1+(size/3)
        # print("text",x1,y1)
        SVGDOCUMENT += f'<text x="{x1}" y="{y1}" fill="{color}" font-face="sans" font-size="{size}" text-anchor="end">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphTextRotate(self, textValue, x, y, size, degrees, color):
        SVGDOCUMENT = ""
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        # y1=y1+(size/3)
        SVGDOCUMENT += f'<text x="{x1}" y="{y1}" fill="{color}" font-face="sans" font-size="{size}"  transform="rotate({degrees} {x1},{y1})">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphDualPolarLine(self, x, y, radius1, startAngle1, radius2, startAngle2, width, color):
        # x = x * self.dpi
        # y = y * self.dpi
        radius1 = radius1 * self.dpi
        radius2 = radius2 * self.dpi
        width = width * self.dpi

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # - self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)  # + self.cartCenterY
        startX, startY = self.polarToCartesian(x, y, radius2, startAngle2)
        endX, endY = self.polarToCartesian(x, y, radius1, startAngle1)
        SVGDOCUMENT = f'<line x1="{startX}" y1="{startY}" x2="{endX}" y2="{endY}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphPolarLine(self, x, y, radius, startAngle,  width, color):
        x = x * self.dpi
        y = y * self.dpi
        radius = radius * self.dpi
        width = float(width) * self.dpi * 1.0

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # - self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)  # + self.cartCenterY
        # startX, startY = self.polarToCartesian(x, y, radius, endAngle)
        endX, endY = self.polarToCartesian(x, y, radius, startAngle)
        SVGDOCUMENT = f'<line x1="{x}" y1="{y}" x2="{endX}" y2="{endY}" style="stroke: {color}; stroke-width: {width};" />\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def drawArc(self, x, y, radius, startAngle, endAngle, width, color):
        x = x * self.dpi
        y = y * self.dpi
        radius = radius * self.dpi
        # print("width", width,"dpi", self.dpi)
        strokeWidth = float(width) * float(self.dpi) * 1.0

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # -self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        startX, startY = self.polarToCartesian(x, y, radius, endAngle)
        endX, endY = self.polarToCartesian(x, y, radius, startAngle)
        if (endAngle - startAngle <= 180):
            largeArcFlag = 0
        else:
            largeArcFlag = 1
        # largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
        # <path id="arc1" fill="none" stroke="#446688" stroke-width="2" d="M 40 20 A 20 20 0 0 0 34.14213562373095 5.857864376269051" onclick="doit();"></path>
        SVGDOCUMENT = f'<path fill="none" stroke="{color}" stroke-width="{strokeWidth}" '
        # "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
        SVGDOCUMENT += f'd="M {startX} {startY} A {radius}, {radius}, 0, {largeArcFlag}, 0,  {endX}, {endY}"'
        SVGDOCUMENT += "></path>\n"

        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def graphArc(self, x, y, radius, startAngle, endAngle, width, color):
        radius = radius * self.dpi
        width = width * self.dpi

        x = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth)  # - self.cartCenterX
        y = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY)  # + self.cartCenterY
        startX, startY = self.polarToCartesian(x, y, radius, endAngle)
        endX, endY = self.polarToCartesian(x, y, radius, startAngle)

        if (endAngle - startAngle <= 180):
            largeArcFlag = 0
        else:
            largeArcFlag = 1
        # largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
        # <path id="arc1" fill="none" stroke="#446688" stroke-width="2" d="M 40 20 A 20 20 0 0 0 34.14213562373095 5.857864376269051" onclick="doit();"></path>
        SVGDOCUMENT = f'<path fill="none" stroke="{color}" stroke-width="{width}" '
        # "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
        SVGDOCUMENT += f'd="M {startX} {startY} A {radius}, {radius}, 0, {largeArcFlag}, 0,  {endX}, {endY}"'
        SVGDOCUMENT += "></path>\n"

        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def output(self):
        return self.document

    def graphPolarText(self, textValue, x, y, degrees, distance, size, color, flip = False):
        SVGDOCUMENT = ""
        distance = distance * self.dpi

        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX+self.physicalWidth)  # -(self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY+self.physicalHeight, self.startY)  # +self.cartCenterY
        # y1=y1+(size/3)
        polarX, polarY = self.polarToCartesian(x1, y1, distance, degrees)
        x1 = polarX
        y1 = polarY
        if flip is True:
            degrees = degrees + 180
        # SVGDOCUMENT += f'<text x="{x1}" y="{y1}" transform="rotate({degrees} {x1},{y1})" fill="{color}" font-face="sans" font-size="{size}">{textValue}</text>\n'
        SVGDOCUMENT += f'<text nox="{x1}" noy="{y1}" transform="translate( {x1},{y1}) rotate({degrees}) " fill="{color}" font-family="DejaVu Sans Mono" font-size="{size}">{textValue}</text>\n'
        self.document += SVGDOCUMENT
        return SVGDOCUMENT

    def circle_line_segment_intersection(self,circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
        """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.
        https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
        :param circle_center: The (x, y) location of the circle center
        :param circle_radius: The radius of the circle
        :param pt1: The (x, y) location of the first point of the segment
        :param pt2: The (x, y) location of the second point of the segment
        :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
        :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
        :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.

        Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html
        """

        (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
        (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
        dx, dy = (x2 - x1), (y2 - y1)
        dr = (dx ** 2 + dy ** 2)**.5
        big_d = x1 * y2 - x2 * y1
        discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

        if discriminant < 0:  # No intersection between circle and line
            return []
        else:  # There may be 0, 1, or 2 intersections with the segment
            intersections = [
                (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
                 cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
                for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
            if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
                fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
                intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
            if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
                return [intersections[0]]
            else:
                return intersections