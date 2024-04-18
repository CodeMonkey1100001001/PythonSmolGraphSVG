# PythonSmolGraphSVG.py
# very simple python to basic plain SVG generator
# useful for making parametric graphs for inkscape.
# Version 20230828.0712
# SVG is normally 0,0 at upper left corner this lib
# is set to use 0,0 and a normal cartesian grid with +x,+y in
# the upper right quadrant and -x,-y in the lower left.

import math


class SmolGraphFancy:
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
        if units == "cm":
            self.dpi = 96/2.54
        if units == "px":
            self.dpi = 1
        self.document = ""
        self.textCirclePathCount = 0
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


    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}')
        fromRange = fromHigh - fromLow
        toRange = toHigh - toLow
        scaleFactor = toRange / fromRange
        tmpValue = value - fromLow
        tmpValue *= scaleFactor
        # print(f'val={value},fromLow={fromLow},fromHigh={fromHigh},toLow={toLow},toHigh={toHigh}, returnValue={tmpValue} toLow={toLow}')
        return tmpValue + toLow

    def setSize(self, physicalWidth, physicalHeight, minX, maxX, minY, maxY):
        self.physicalWidth = physicalWidth * self.dpi
        self.physicalHeight = physicalHeight * self.dpi
        self.minValueX = minX
        self.maxValueX = maxX
        self.minValueY = minY
        self.maxValueY = maxY

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

    def graphTextOnACircle(self, text, x, y, radius, clockwise=True, rotation=0, extraTextInfo='', textAnchor = "start"):

        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        radius = radius * self.dpi

        self.textCirclePathCount += 1
        offset = rotation / 360 * 100  # rotation in in 0-360 but offset is in %
        path_id_text = f'textcirclepath{self.textCirclePathCount}'
        if clockwise:
            sweep_flag = 1
        else:
            sweep_flag = 0

        # Path definition: This draws a full circle (360 degrees)
        circle_path = f'<defs><path id="{path_id_text}" fill="transparent" stroke="transparent" d="M {x1} {y1 - radius} A {radius} {radius} 0 1 {sweep_flag} {x1} {y1 + radius} A {radius} {radius} 0 1 {sweep_flag} {x1} {y1 - radius}" transform="rotate(-45 {x1} {y1})" /></defs>'
        # Text styling and alignment along the path
        # Adjust the `startOffset` to control the starting position of the text
        text_style = f'''
        <text fill="{self.color}" font-family="{self.fontFamily}" font-size="{self.fontSize}" {extraTextInfo}>
            <textPath xlink:href="#{path_id_text}" startOffset="{offset}%" style="text-anchor: {textAnchor};" dominant-baseline="{textAnchor}" >{text}</textPath>
        </text>'''

        # Combine all parts to form the final SVG
        svg_content = f'{circle_path}\n{text_style}\n'
        return svg_content

    def graphTextOnACircleMid(self, text, x, y, radius, rotation=0, clockwise=True, extraTextInfo=''):
        x1 = self.map(x, self.minValueX, self.maxValueX, self.startX, self.startX + self.physicalWidth) + (self.cartCenterX)
        y1 = self.map(y, self.minValueY, self.maxValueY, self.startY + self.physicalHeight, self.startY) - self.cartCenterY
        radius = radius * self.dpi
        rotation = 180 + rotation

        self.textCirclePathCount += 1
        #offset = rotation / 360 * 100  # rotation in in 0-360 but offset is in %
        path_id_text = f'textcirclepath{self.textCirclePathCount}'
        if clockwise:
            sweep_flag = 1
        else:
            sweep_flag = 0

        # Path definition: This draws a full circle (360 degrees)
        circle_path = f'<defs><path id="{path_id_text}" fill="transparent" stroke="transparent" d="M {x1} {y1 - radius} A {radius} {radius} 0 1 {sweep_flag} {x1} {y1 + radius} A {radius} {radius} 0 1 {sweep_flag} {x1} {y1 - radius}" transform="rotate({rotation} {x1} {y1})" /></defs>'

        # Text styling and alignment along the path
        # Adjust the `startOffset` to control the starting position of the text
        text_style = f'''
        <text fill="{self.color}" font-family="{self.fontFamily}" font-size="{self.fontSize}" {extraTextInfo}>
            <textPath xlink:href="#{path_id_text}" startOffset="50%" style="text-anchor: middle;" dominant-baseline="middle" >{text}</textPath>
        </text>'''

        # Combine all parts to form the final SVG
        svg_content = f'{circle_path}\n{text_style}\n'
        return svg_content

