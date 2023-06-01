from tkinter import *
from R2Graph import *
from LeastSquaresPol import *
import math

def main():
    points = []
    mouseButtons = []
    objectIDs = []
    catchedPoint = (-1) # Index of catched point in points array    
    funcDrawn = False
    coeffs = []
    plotID = (-1)
    
    scaleX = 40.; scaleY = 40.
    root = Tk()
    root.title("Interpolation Polynomial")
    root.geometry("800x600")
    panel = Frame(root)
    drawButton = Button(panel, text="Draw")
    clearButton = Button(panel, text="Clear")
    drawArea = Canvas(root, bg="white")
    
    panel.pack(side=TOP, fill=X)
    drawButton.pack(side=LEFT, padx=4, pady=4)    
    clearButton.pack(side=LEFT, padx=4, pady=4)
    drawArea.pack(side=TOP, fill=BOTH, expand=True, padx=4, pady=4)
    
    degree = 1
    degreeLabel = Label(panel, text="Degree:")
    scale = Scale(panel, from_=1, to=10, orient=HORIZONTAL)
    
    degreeLabel.pack(side=LEFT, padx=4, pady=4)
    scale.pack(side=LEFT, padx=4, pady=4)
    
    def map(t):
        w = drawArea.winfo_width()
        h = drawArea.winfo_height()
        centerX = w/2.
        centerY = h/2.
        x = centerX + t.x*scaleX
        y = centerY - t.y*scaleY
        return (x, y)
        
    def invmap(p):
        w = drawArea.winfo_width()
        h = drawArea.winfo_height()
        centerX = w/2.
        centerY = h/2.
        x = (p[0] - centerX)/scaleX
        y = (centerY - p[1])/scaleY
        return R2Point(x, y)
        
    def xMin():
        w = drawArea.winfo_width()
        return (-(w/scaleX)/2.)
    def xMax():
        return (-xMin())
    def yMin():
        w = drawArea.winfo_height()
        return (-(w/scaleY)/2.)
    def yMax():
        return (-yMin())
        
    def drawGrid():
        ix0 = int(xMin())
        ix1 = int(xMax())
        x = ix0
        while x <= ix1:
            if x != 0:
                p0 = map(R2Point(x, yMin()))
                p1 = map(R2Point(x, yMax()))
                drawArea.create_line(p0, p1, fill="lightGray", width=1)
            x += 1

        iy0 = int(yMin())
        iy1 = int(yMax())
        y = iy0
        while y <= iy1:
            if y != 0:
                p0 = map(R2Point(xMin(), y))
                p1 = map(R2Point(xMax(), y))
                drawArea.create_line(p0, p1, fill="lightGray", width=1)
            y += 1
            
        # Draw x-axis
        drawArea.create_line(
            map(R2Point(xMin(), 0.)), map(R2Point(xMax(), 0.)),
            fill="black", width=2
        )    
        # Draw y-axis
        drawArea.create_line(
            map(R2Point(0., yMin())), map(R2Point(0., yMax())),
            fill="black", width=2
        )
        
    def plotFunction():
        nonlocal funcDrawn, plotID, degree
        dx = 0.05
        path = []
        if plotID >= 0:
            drawArea.delete(plotID)
            plotID = (-1)       
        y = leastSquaresValue(coeffs, xMin())
        t = R2Point(xMin(), y)
        while t.x <= xMax():
            path.append(map(t))
            t.x += dx
            t.y = leastSquaresValue(coeffs, t.x)
        plotID = drawArea.create_line(path, fill="blue", width=2)
        funcDrawn = True
        
    def onMouseRelease(e):
        nonlocal catchedPoint, coeffs, degree
        p = (e.x, e.y)
        t = invmap(p)
        if catchedPoint < 0:
            points.append(t)
            mouseButtons.append(e.num)
            drawPoint(t, e.num)
        else:
            points[catchedPoint] = t
            if funcDrawn:
                coeffs = computeLeastSquaresPol(points, degree)
            redraw()
            catchedPoint = (-1)
            drawArea.configure(cursor="")
        
    def drawPoint(t, mouseButton = 1):
        vx = R2Vector(0.3, 0.)
        vy = R2Vector(0., 0.3)
        color = "red"
        if mouseButton == 2:
            color = "green"
        elif mouseButton == 3:
            color = "magenta"
        lineID = drawArea.create_line(
            map(t - vx), map(t + vx), fill=color, width=3
        )
        objectIDs.append(lineID)    
        lineID = drawArea.create_line(
            map(t - vy), map(t + vy), fill=color, width=3
        )    
        objectIDs.append(lineID)
        
    def drawPoints():
        for i in range(len(points)):
            drawPoint(points[i], mouseButtons[i])
        
    def onDraw():
        nonlocal coeffs, degree
        if len(points) > 0:
            degree = scale.get() # get degree from the scale widget
            coeffs = computeLeastSquaresPol(points, degree)
            plotFunction()

    def clearPicture():         
        nonlocal plotID
        for i in objectIDs:
            drawArea.delete(i)
        objectIDs.clear()
        if plotID >= 0:
            drawArea.delete(plotID)
            plotID = (-1)

    def redraw():
        clearPicture()
        drawPoints()
        if funcDrawn:
            plotFunction()

    def onClear():
        nonlocal funcDrawn
        clearPicture()
        points.clear()
        mouseButtons.clear()
        funcDrawn = False

    def onConfigure(e):
        drawArea.delete("all")
        drawGrid()
        if funcDrawn:
            plotFunction()    
        drawPoints()         

    def findPoint(t):
        distanceThreshold = 0.2
        minDist = 1e+30     # + infinity
        minPointIdx = (-1)
        for i in range(len(points)):
            d = t.distance(points[i])
            if d < minDist:
                minDist = d; minPointIdx = i
        if minDist <= distanceThreshold:
            return minPointIdx
        else:
            return (-1)
            
    def onMouseMotion(e):
        nonlocal plotID, coeffs
        t = invmap((e.x, e.y))
        if catchedPoint >= 0:
            points[catchedPoint] = t
            if funcDrawn:
                coeffs = computeNewtonPol(points)
            redraw()
        else:
            pointIdx = findPoint(t)
            if pointIdx >= 0:
                drawArea.configure(cursor="hand1")
            else:
                drawArea.configure(cursor="")
                
    def onMousePress(e):
        nonlocal catchedPoint
        t = invmap((e.x, e.y))
        pointIdx = findPoint(t)
        if pointIdx >= 0:
            catchedPoint = pointIdx;
            drawArea.configure(cursor="sailboat")                

    drawButton.configure(command = onDraw)
    clearButton.configure(command = onClear)
    drawArea.bind("<ButtonRelease-1>", onMouseRelease)
    drawArea.bind("<ButtonRelease-2>", onMouseRelease)
    drawArea.bind("<ButtonRelease-3>", onMouseRelease)
    drawArea.bind("<Configure>", onConfigure)
    drawArea.bind("<Button-1>", onMousePress)
    drawArea.bind("<Motion>", onMouseMotion)

    drawGrid()

    root.mainloop()

if __name__ == "__main__":
    main()
