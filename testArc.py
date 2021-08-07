import PythonSmolGraphSVG

sg = PythonSmolGraphSVG.SmolGraph2SVG("inch")
sg.svgHeader()
sg.graphCircle(0,0,2 ,0.1, "red")
sg.graphLine(0,0,2,2,0.05,"black")

sg.drawArc(0,0,2.5,0,45,0.05,"red")
sg.graphArc(0.0,0.0,1.0,0,180,0.05,"black")

#Fancy Ellipse
sg.graphArc(1.5,1.5,1.0,0,180,0.05,"black")
sg.graphArc(-1.5,1.5,1.0,180,360,0.05,"black")
x1,y1 = sg.polarToCartesian(1.5, 1.5, 1.0, 0)
x2,y2 = sg.polarToCartesian(-1.5, 1.5, 1.0, 0)
sg.graphLine(x1,y1,x2,y2,0.05,"black")
x1,y1 = sg.polarToCartesian(1.5, 1.5, 1.0, 180)
x2,y2 = sg.polarToCartesian(-1.5, 1.5, 1.0, 180)
sg.graphLine(x1,y1,x2,y2,0.05,"black")


sg.svgFooter()

fp = open("/tmp/misc/test.svg","w")
fp.writelines(sg.output())
fp.close()

print(sg.output())
print("x1",x1,"y1",y1)
print("x2",x2,"y2",y2)


