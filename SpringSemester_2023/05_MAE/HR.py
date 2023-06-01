from tkinter import *
from R2Graph import *
import math
import numpy as np
from sklearn.linear_model import HuberRegressor, LinearRegression
from scipy.optimize import linprog
import cvxpy as cp

def mae_regression_cvx(a, y):
    n = a.shape[1]
    beta = cp.Variable(n)
    objective = cp.Minimize(cp.norm(a @ beta - y, 1))
    problem = cp.Problem(objective)
    problem.solve()
    return beta.value

def func(p, x):
    return np.polyval(p, x)

def mae_regression(a, y):
    num_vars = len(a[0]) + len(a)
    num_constraints = len(a)
    c = [0]*len(a[0]) + [1]*len(a)
    bounds = [(None, None)]*len(a[0]) + [(0, None)]*len(a)
    A = []
    for i in range(num_constraints):
        A.append(list(a[i]) + [-1]*i + [-1] + [0]*(num_constraints-i-1))
        A.append(list(a[i]) + [0]*i + [1] + [0]*(num_constraints-i-1))
    b = list(y) + list(y)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    return res.x[:len(a[0])]

def main():
    points = []
    mouseButtons = []
    objectIDs = []
    linearPlotID = (-1)
    huberPlotID = (-1)
    pol = np.array([])

    scaleX = 40.; scaleY = 40.
    root = Tk()
    root.title("Linear Regression")
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
    scale.set(degree)
    degreeLabel.pack(side=LEFT, padx=4, pady=4)
    scale.pack(side=LEFT, padx=4, pady=4)

    lossFunctionIdx = IntVar(value = 0)
    lossFunctionMSERadio = Radiobutton(
        panel,
        text = "MSE", variable=lossFunctionIdx, value=0,
        fg = "darkBlue"
    )
    lossFunctionHuberRadio = Radiobutton(
        panel,
        text = "Huber", variable=lossFunctionIdx, value=1,
        fg = "darkRed"
    )
    lossFunctionMSERadio.pack(side=LEFT, padx=4, pady=4)
    lossFunctionHuberRadio.pack(side=LEFT, padx=4, pady=4)

    root.update()

    maePlotID = (-1)

    lossFunctionMAERadio = Radiobutton(
        panel,
        text = "MAE", variable=lossFunctionIdx, value=2,
        fg = "darkGreen"
    )
    lossFunctionMAERadio.pack(side=LEFT, padx=4, pady=4)


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
        nonlocal linearPlotID, huberPlotID, maePlotID
        if len(pol) == 0:
            return

        lossFunc = lossFunctionIdx.get()
        if lossFunc == 0:
            color = "blue"
        elif lossFunc == 1:
            color = "red"
        else:
            color = "darkGreen"
        t = R2Point(xMin(), func(pol, xMin()))
        dx = 0.05
        path = []
        while t.x <= xMax():
            path.append(map(t))
            t.x += dx
            t.y = func(pol, t.x)
        plotID = drawArea.create_line(path, fill=color, width=2)
        if lossFunc == 0:
            linearPlotID = plotID
        elif lossFunc == 1:
            huberPlotID = plotID
        else:
            maePlotID = plotID
        
    def onMouseRelease(e):
        # print("Mouse release event:", e)
        p = (e.x, e.y)
        t = invmap(p)
        points.append(t)
        mouseButtons.append(e.num)
        drawPoint(t, e.num)
        
    def drawPoint(t, mouseButton = 1):
        vx = R2Vector(0.2, 0.)
        vy = R2Vector(0., 0.2)
        color = "red"
        if mouseButton == 2:
            color = "green"
        elif mouseButton == 3:
            color = "magenta"
        lineID = drawArea.create_line(
            map(t - vx), map(t + vx), fill=color, width=2
        )
        objectIDs.append(lineID)    
        lineID = drawArea.create_line(
            map(t - vy), map(t + vy), fill=color, width=2
        )    
        objectIDs.append(lineID)
        
    def drawPoints():
        for i in range(len(points)):
            drawPoint(points[i], mouseButtons[i])
        
    def onDraw():
        nonlocal pol, degree, linearPlotID, huberPlotID, maePlotID
        lossFunc = lossFunctionIdx.get()

        if lossFunc == 0 and linearPlotID >= 0:
            drawArea.delete(linearPlotID)
        elif lossFunc == 1 and huberPlotID >= 0:
            drawArea.delete(huberPlotID)
        elif lossFunc == 2 and maePlotID >= 0:
            drawArea.delete(maePlotID)

        degree = scale.get()
        m = len(points)
        if m == 0:
            return
        y = np.array([points[i].y for i in range(m)])
        print("y =", y)
        a = np.vander([points[i].x for i in range(m)], degree + 1)
        print("a =", a)

        if lossFunc == 0:
            linear_reg = LinearRegression(fit_intercept=False)
            y = y.reshape([-1, 1])
            linear_reg.fit(a, y)
            pol = [linear_reg.coef_[0][i] for i in range(degree + 1)]
        elif lossFunc == 1:
            huber_reg = HuberRegressor(fit_intercept=False)
            huber_reg.fit(a, y)
            pol = [huber_reg.coef_[i] for i in range(degree + 1)]
        else:
            pol = mae_regression_cvx(a, y)

        print("pol =", pol)
        plotFunction()

        
    def clearPicture():
        nonlocal linearPlotID, huberPlotID, maePlotID
        for i in objectIDs:
            drawArea.delete(i)
        objectIDs.clear()
        if linearPlotID >= 0:
            drawArea.delete(linearPlotID)
            linearPlotID = (-1)
        if huberPlotID >= 0:
            drawArea.delete(huberPlotID)
            huberPlotID = (-1)
        if maePlotID >= 0:
            drawArea.delete(maePlotID)
            maePlotID = (-1)

    def onClear():
        nonlocal linearPlotID, huberPlotID, maePlotID
        clearPicture()
        points.clear()
        mouseButtons.clear()
        linearPlotID = (-1) 
        huberPlotID = (-1)
        maePlotID = (-1)

        
    def onConfigure(e):
        drawArea.delete("all")
        drawGrid()
        drawPoints()        

    drawButton.configure(command = onDraw)
    clearButton.configure(command = onClear)
    scale.configure(command = lambda e: onDraw())
    drawArea.bind("<ButtonRelease-1>", onMouseRelease)
    drawArea.bind("<ButtonRelease-2>", onMouseRelease)
    drawArea.bind("<ButtonRelease-3>", onMouseRelease)
    drawArea.bind("<Configure>", onConfigure)
    
    drawGrid()
    # plotFunction()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()     
