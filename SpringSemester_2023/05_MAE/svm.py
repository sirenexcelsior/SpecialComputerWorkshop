from tkinter import *
from R2Graph import *
import math
import numpy as np
from sklearn.svm import SVC
from copy import deepcopy
from scipy.optimize import minimize
from tkinter import *
import math
import numpy as np
from copy import deepcopy
from scipy.optimize import minimize

# Add the following import statement
from skimage import measure

# Rest of the code...


SCALEX = 40.
SCALEY = SCALEX

STEPX = 3. / SCALEX  # 3 pixels
STEPY = 3. / SCALEX


def main():
    points = []
    mouseButtons = []
    objectIDs = []
    levelLineIDs = []

    # Parameters of linear classifier:
    w = np.array([0., 0.])  # Normal vector to the hyperplane
    b = 0.  # Intercept

    def linearClassifier(x):
        """Value of the linear classifier
        at the point x"""
        return w @ x - b

    scaleX = SCALEX
    scaleY = SCALEY
    root = Tk()
    root.title("Support Vector Machine")
    root.geometry("860x600")
    panel = Frame(root)
    drawButton = Button(panel, text="Draw")
    clearButton = Button(panel, text="Clear")
    drawArea = Canvas(root, bg="white")
    panel.pack(side=TOP, fill=X)
    drawButton.pack(side=LEFT, padx=4, pady=4)
    clearButton.pack(side=LEFT, padx=4, pady=4)
    drawArea.pack(side=TOP, fill=BOTH, expand=True, padx=4, pady=4)
    cLabel = Label(panel, text="C:")
    scaleC = Scale(
        panel, from_=0.1, to=20., resolution=0.1,
        orient=HORIZONTAL, length=200
    )
    scaleC.set(10.)
    cLabel.pack(side=LEFT, padx=4, pady=4)
    scaleC.pack(side=LEFT, padx=4, pady=4)

    kernelLabel = Label(panel, text="Kernel:")
    kernelLabel.pack(side=LEFT, padx=4, pady=4)

    kernelIdx = IntVar()  # Control variable for the group of radio buttons
    kernelIdx.set(0)
    kernel = 'linear'

    def setKernel():
        nonlocal kernel
        idx = kernelIdx.get()
        if idx == 0:
            kernel = 'linear'
        elif idx == 1:
            kernel = 'rbf'
        elif idx == 2:
            kernel = 'poly'
        # if len(points) > 0:
        #    onDraw()

    linearRadio = Radiobutton(
        panel,
        text="Linear", variable=kernelIdx, value=0,
        command=setKernel
    )
    rbfRadio = Radiobutton(
        panel,
        text="RBF", variable=kernelIdx, value=1,
        command=setKernel
    )
    polyRadio = Radiobutton(
        panel,
        text="Poly", variable=kernelIdx, value=2,
        command=setKernel
    )

    linearRadio.pack(side=LEFT, padx=4, pady=4)
    rbfRadio.pack(side=LEFT, padx=4, pady=4)
    polyRadio.pack(side=LEFT, padx=4, pady=4)

    def classifierFunction(x, y):
        p = np.array([[x, y]], dtype="float64")
        return clf.predict(p)[0]

    root.update()

    def map(t):
        w = drawArea.winfo_width()
        h = drawArea.winfo_height()
        centerX = w / 2.
        centerY = h / 2.
        x = centerX + t.x * scaleX
        y = centerY - t.y * scaleY
        return (x, y)

    def invmap(p):
        w = drawArea.winfo_width()
        h = drawArea.winfo_height()
        centerX = w / 2.
        centerY = h / 2.
        x = (p[0] - centerX) / scaleX
        y = (centerY - p[1]) / scaleY
        return R2Point(x, y)

    def xMin():
        w = drawArea.winfo_width()
        return (-(w / scaleX) / 2.)

    def xMax():
        return (-xMin())

    def yMin():
        w = drawArea.winfo_height()
        return (-(w / scaleY) / 2.)

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

    def onMouseRelease(e):
        # print("Mouse release event:", e)
        p = (e.x, e.y)
        t = invmap(p)
        points.append(t)
        mouseButtons.append(e.num)
        drawPoint(t, e.num)

    def drawPoint(t, mouseButton=1):
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

    def drawLevelLine(f, clf, level=0., color="blue"):
        nonlocal levelLineIDs
        levelLineIDs.clear()

        x0 = xMin()
        x1 = xMax()
        y0 = yMin()
        y1 = yMax()
        y = y0
        a = []
        while y <= y1:
            row = []
            x = x0
            while x <= x1:
                z = f(x, y, clf)
                row.append(z)
                x += STEPX
            a.append(row)
            y += STEPY
        a = np.array(a)

        contours = measure.find_contours(a, level)
        for contour in contours:
            line = []
            for p in contour:
                x = x0 + p[1] * STEPX
                y = y0 + p[0] * STEPY
                line.append(
                    map(R2Point(x, y))
                )
            lineID = drawArea.create_line(line, width=2, fill=color)
            levelLineIDs.append(lineID)


    def onDraw():
        if len(points) == 0:
            return

        for i in levelLineIDs:
            drawArea.delete(i)
        levelLineIDs.clear()

        data = [
            [points[i].x, points[i].y, 1. if mouseButtons[i] == 1 else (-1.)]
            for i in range(len(points))
        ]
        c = scaleC.get()
        print("C =", c)
        clf = SVC(C=c, kernel=kernel)
        X = np.array([[d[0], d[1]] for d in data])
        y = np.array([d[2] for d in data])
        clf.fit(X, y)

        drawLevelLine(classifierFunction, clf, 0.)

        if kernel == 'linear':
            w = clf.coef_[0]
            b = clf.intercept_
        else:
            # For non-linear kernels, use decision_function to get distances to the separating hyperplane
            xx, yy = np.meshgrid(np.linspace(xMin(), xMax(), 500),
                                 np.linspace(yMin(), yMax(), 500))
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)

            drawArea.contour(xx, yy, Z, colors='blue', levels=[0], linestyles='dashed', linewidths=2)


    def classifierFunction(x, y, clf):
        p = np.array([[x, y]], dtype="float64")
        return clf.predict(p)[0]


    def clearPicture():
        for i in objectIDs:
            drawArea.delete(i)
        objectIDs.clear()

        for i in levelLineIDs:
            drawArea.delete(i)
        levelLineIDs.clear()

    def onClear():
        clearPicture()
        points.clear()
        mouseButtons.clear()

    def onConfigure(e):
        drawArea.delete("all")
        drawGrid()
        drawPoints()

    drawButton.configure(command=onDraw)
    clearButton.configure(command=onClear)
    drawArea.bind("<ButtonRelease-1>", onMouseRelease)
    drawArea.bind("<ButtonRelease-2>", onMouseRelease)
    drawArea.bind("<ButtonRelease-3>", onMouseRelease)
    drawArea.bind("<Configure>", onConfigure)

    drawGrid()

    root.mainloop()


if __name__ == "__main__":
    main()
