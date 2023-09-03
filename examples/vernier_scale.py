# from pprint import pprint
import PythonSmolGraphSVG
import PythonSmolGraphFancyStuff

# vernier scale 1/10 inches

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

sg = PythonSmolGraphSVG.SmolGraph2SVG("inch")
sgf = PythonSmolGraphFancyStuff.SmolGraphFancy("inch")

sg.setSize(20, 20, -10, 10, -10, 10)
# sg.setCenter(-10,-10)

theDoc = sg.svgHeader()
# drawGrid()

theDoc += "<g>\n"

for i in range(0,100):
    inchMark = i/10
    theHeight = (2/8)
    # print("inchMark", inchMark, inchMark % 1)
    if inchMark % 0.5 == 0:
        theHeight = 3/8
    if inchMark % 1 == 0:
        theHeight = 4/8
        theDoc += sg.graphText(str(int(inchMark)),inchMark,-(1/8),"8pt",textAnchor="middle")
    theDoc += sg.graphLine(inchMark,0,inchMark,theHeight,width=0.01)
theDoc += sg.graphText("Decimal Inches",0,0.55,"6pt")
theDoc += "</g>\n"

theDoc += "<g>\n"
for i in range(0,11):
    inchMark = i/10 - (i*0.01)
    theHeight = (2/8)
    # print("inchmark", inchMark, inchMark % 1)
    theDoc += sg.graphText(str(int(i)),inchMark,1+(11/16),"6pt",textAnchor="middle")
    theDoc += sg.graphLine(inchMark,2.00,inchMark,2.0-theHeight,width=0.01)
theDoc += sg.graphText("0.01",1.1,1.8,"6pt")
theDoc += "</g>\n"

# theDoc += sg.graphArc(0, 0, 7, 45, 45 + 90, 0.2, "#FF00FF")
# theDoc += sg.graphRectangle(-4, -4, -3, -3, 0.1, "#770737")
# theDoc += sg.graphRectangleFilled(-4, -5, -3, -4, "#F33A6A", 0.1, "#0000cc")
# theDoc += sg.graphCircle(-5, 5, 1.0, 0.2, "#0000ff")
# theDoc += sg.graphDisk(-5, 3, 1.0, "#00ccff")
# theDoc += sg.graphDiskText(-5, 1, 1.0, "disk text", "#0000cc")  # graph a disc but with hover help
# theDoc += sg.graphText("PlainText", 4, -5, "24pt", "#cc0000")
# theDoc += sg.graphTextRotate("Rotated66", 4, -5, "12pt", 66, "#cc00cc")
# theDoc += sg.graphDualPolarLine(0, 0, 2.5, 66, 3.0, 67, 0.1, "#ff4444")
# theDoc += sg.graphPolarLine(0, 0, 9.5, 12, 0.1, "#cc4433")
# # theDoc += sg.drawArc(4,-4,2,45,45+90,0.1,"#fafa00")
# theDoc += sg.graphArc(4.5, -4.5, 2, 45, 45 + 90, 0.1, "#fafa00")
# theDoc += sg.graphLine(-5, -9, 5, -9)  # test using defaults for width and color

# test font-family change
sg.fontFamily = "sans"
theDoc += sg.graphText("PlainSansText", 4.5, -6, "24pt", "#cc0000")
theDoc += sg.svgFooter()

fp = open("/tmp/misc/test.svg", "w")
fp.writelines(theDoc)
fp.close()

# print(theDoc)

print(sg.getSizeHuman())
