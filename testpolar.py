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

import math

def cartesianToPolar(x, y):
    theRadians = math.atan2(x, y)
    #theDegrees = math.degrees(theRadians)
    #theDegrees = (180 / 3.14159265359) * theRadians
    theDegrees = (180 / math.pi) * theRadians
    if (theDegrees < 0):
        theDegrees = 360 + theDegrees
    theRadius=math.sqrt((x * x) + (y * y))
    return theDegrees, theRadius


#Polar to Cartesian formula.
def polarToCartesian(centerX, centerY, radius, angleInDegrees):
   angleInRadians = math.radians(angleInDegrees)
   # angleInRadians = angleInDegrees  * 3.14159265359 / 180.0 # manual method
   x = centerX + (radius * math.sin(angleInRadians))
   y = centerY + (radius * math.cos(angleInRadians))
   return x, y


def testBackAndForth(x, y):
    cartesianX = x
    cartesianY = y
    print("cartesianX", cartesianX, "cartesianY", cartesianY)
    polarDegrees, polarRadius  = cartesianToPolar(cartesianX, cartesianY )
    print("polarDegrees",polarDegrees, "polarRadius", polarRadius)

    cartesianX , cartesianY = polarToCartesian(0,0, polarRadius, polarDegrees)
    cartesianX = round(cartesianX, 5)
    cartesianY = round(cartesianY, 5)
    print("cartesianX", cartesianX, "cartesianY", cartesianY)
    returnValue = 0
    if cartesianX == x and cartesianY == y:
        print("TRUE")
        returnValue = 1
    else:
        print("False !!!!!!!!!!!!!!")
    print("===============")
    return returnValue

allTestCount = 0
numberOfTests = 8
allTestCount += testBackAndForth(5,5)
allTestCount += testBackAndForth(-5,-5)
allTestCount += testBackAndForth(10,5)
allTestCount += testBackAndForth(-108.33,235.35)
allTestCount += testBackAndForth(0,0)
allTestCount += testBackAndForth(0,101.001)
allTestCount += testBackAndForth(101.11,-0)
allTestCount += testBackAndForth(-10191.88,-762.80)
if (allTestCount == numberOfTests):
    print("========All tests passed")
else:
    print("========FAIL!!!!!")
