import PythonSmolGraphSVG

def drawGrid():
    global theDoc
    x=sg.minValueX
    #print("x minValueX",x,sg.minValueX)
    #print("sg.minValueY",sg.minValueY,sg.maxValueY)
    while x < sg.maxValueX:
        #print("x",x)
        theDoc += sg.graphLine(x, sg.minValueY, x, sg.maxValueY, 0.05, "#5f9b9c")
        x = x + 1.0

    y = sg.minValueY
    while y < sg.maxValueY:
        theDoc += sg.graphLine(sg.minValueX, y, sg.maxValueX, y, 0.05, "#5f9b9c")
        y = y + 1.0

    theDoc += sg.graphLine(sg.minValueX, 0, sg.maxValueX, 0, 0.1, "red")
    theDoc += sg.graphLine(0, sg.minValueY, 0, sg.maxValueY, 0.1, "green")


print("hello")

sg = PythonSmolGraphSVG.SmolGraph2SVG("inch")

#sg=SmolGraph2SVG()



theDoc = sg.svgHeader()
#drawGrid()

# cartX, cartY = sg.polarToCartesian(0,0,100,90)
#theDoc += sg.graphLine(0,0,1.0,1.0,0.1,"green")
#theDoc += sg.graphLine(0,0,1.0,0.0,0.1,"blue")
#
# cartX, cartY = sg.polarToCartesian(0,0,100,180)
# theDoc += sg.graphLine(0,0,cartX,cartY,2.0,"blue")

subDivisions = 360/16
minorRadius = 1
majorRadius = 2

subSteps = 7

degreesBetween = (360 / subDivisions) - 7

lineWidth = 0.016
lineColor = "black"

i = 0
while i < 90:
    #print(i)
    #theDoc += sg.drawArc(0,0,100,0,i*1,4.0,"brown")
    #theDoc += sg.drawArc(0,0,40,0,(180/8)*1,4.0,"brown")
    theDoc += sg.graphDualPolarLine(0,0, minorRadius,   i               , majorRadius,  i,                 lineWidth, lineColor)
    theDoc += sg.graphDualPolarLine(0,0, minorRadius,   i + degreesBetween, majorRadius,  i + degreesBetween,  lineWidth, lineColor)
    theDoc += sg.graphArc(0, 0, majorRadius, i, i + degreesBetween, lineWidth, lineColor)
    #theDoc += sg.drawArc(0, 0, minorRadius, i, i + degreesBetween, lineWidth, lineColor)

    subNum = minorRadius
    while subNum < majorRadius:
        #    for subNum in range(minorRadius, majorRadius, int((majorRadius-minorRadius) / subSteps)):
#        #print("subNum",subNum)
        theDoc += sg.graphArc(0,0,subNum,i,i + degreesBetween, lineWidth, lineColor)
        subNum = subNum + ( (majorRadius-minorRadius) / subSteps )
        #theX , theY = sg.polarToCartesianFlip(0,0,subNum-0.18,i+2)
        #theDoc += sg.graphText("0",theX,theY,"#000000",24)
    i = i + (360/subDivisions)


#theDoc += sg.graphDualPolarLine(0,0,40,(180/8)*2, 100,(180/8)* 2, 2.0, "violet")
#theDoc += sg.graphDualPolarLine(0,0,40,(180/8)*3, 100,(180/8)* 3, 2.0, "violet")

#theDoc += sg.graphArc(0, 0, minorRadius * 0.95 , 0,359.9, lineWidth, "red")
theDoc += sg.graphCircle(0,0,minorRadius * 0.95 , lineWidth, "red")
theDoc += sg.graphCircle(0,0,minorRadius * 0.85 , lineWidth, "red")
#theDoc += sg.graphArc(0, 0, minorRadius * 0.85 , 0,359.9, lineWidth, "red")


#theDoc += sg.graphRectangle(0,0,1,1,0.016,"orange")
#theDoc += sg.graphCircle(0,0,4,0.016,"purple")

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




#theDoc += sg.graphDualPolarLine(0,0,2,45,2,90,0.1,"gold")

theDoc += sg.svgFooter()


fp = open("/tmp/misc/test.svg","w")
fp.writelines(theDoc)
fp.close()

print(theDoc)


