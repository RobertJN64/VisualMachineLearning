from MachineLearning import GeneticNets as gn
import matplotlib.pyplot as pyplot
import PythonExtended.Graphing as graph
import PythonExtended.Math as m

#CONFIG
gradconfig = False
config_hidemid = False
config = "all"
#config = "onlyblue"
#config = "onlyorange"
#config = "edge"
#config = "plane"


#region data management funcs
def isCorner(db, x, y, z):
    return (z == 0 or z == len(db) - 1) and (y == 0 or y == len(db[z]) - 1) and (x == 0 or x == len(db[y]) - 1)

def isMid(db,x,y,z):
    return z == 0 or z == len(db) - 1 or y == 0 or y == len(db[z]) - 1 or x == 0 or x == len(db[y]) - 1

def isPlane(x, y, z):
    return x == 10 or y == 10 or z == 10

def getPoint(db, x, y, z):
    if z < 0 or x < 0 or y < 0:
        return 0, False
    if z >= len(db) or y >= len(db[z]) or x >= len(db[z][y]):
        return 0, False
    else:
        return db[z][y][x][0], True

def compare(a, b):
    return (a > 0 and b > 0) or (a <= 0 and b <= 0)

def keepPoint(db, x, y, z, val):
    if (config == "onlyblue" and val <= 0) or (config == "onlyorange" and val > 0):
        return False
    if config == "edge" and isCorner(db, x, y, z):
        return True
    if config == "plane" and isPlane(x,y,z):
        return True
    if (config == "edge" or config == "plane") and val <= 0:
        return False

    points = []
    p, suc = getPoint(db, x - 1, y, z)
    if suc:
        points.append(p)
    p, suc = getPoint(db, x + 1, y, z)
    if suc:
        points.append(p)
    p, suc = getPoint(db, x, y - 1, z)
    if suc:
        points.append(p)
    p, suc = getPoint(db, x, y + 1, z)
    if suc:
        points.append(p)
    p, suc = getPoint(db, x, y, z - 1)
    if suc:
        points.append(p)
    p, suc = getPoint(db, x, y, z + 1)
    if suc:
        points.append(p)


    for point in points:
        if not compare(point, val):
            return True

    if len(points) == 6 and config_hidemid:
        return False

    if config == "all":
        return True

    if (config == "onlyblue" and val > 0) or (config == "onlyorange" and val <= 0):
        return True

    return False

#endregion

class GraphManager:
    def __init__(self, net, xaxis, yaxis, zaxis, plt):
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.zaxis = zaxis

        self.xvals = []
        self.yvals = []
        self.zvals = []
        self.colorvals = []


        self.minv = 0
        self.maxv = 0

        self.points = []
        self.plt = plt

        z = -1
        while z <= 1:
            minilist = []
            y = -1
            while y <= 1:
                miniminilist = []
                x = -1
                while x <= 1:
                    net.reset()
                    for inName in net.inputs:
                        if inName == xaxis:
                            net.setNode(inName, x)
                        elif inName == yaxis:
                            net.setNode(inName, y)
                        elif inName == zaxis:
                            net.setNode(inName, z)
                        else:
                            net.setNode(inName, 0)
                    net.process()
                    out = net.getNode(net.classifier_output)
                    if out > self.maxv:
                        self.maxv = out
                    elif out < self.minv:
                        self.minv = out
                    miniminilist.append([out,0])
                    x += 0.1
                minilist.append(miniminilist)
                y += 0.1
            self.points.append(minilist)
            z += 0.1

    def reduce(self):
        for z in range(0, len(self.points)):
            for y in range(0, len(self.points[z])):
                for x in range(0, len(self.points[y])):
                    val = self.points[z][y][x]
                    if keepPoint(self.points, x, y, z, val[0]):
                        val[1] = 1

    def prep(self):
        for z in range(0, len(self.points)):
            for y in range(0, len(self.points[z])):
                for x in range(0, len(self.points[y])):
                    val = self.points[z][y][x]
                    if val[1] == 1:
                        self.xvals.append(x/10-1)
                        self.yvals.append(y/10-1)
                        self.zvals.append(z/10-1)
                        if not gradconfig:
                            if val[0] > 0:
                                if (config == "edge" and not isCorner(self.points, x, y, z)) or (config == "plane" and not isPlane(x,y,z)):
                                    self.colorvals.append("red")
                                else:
                                    self.colorvals.append("blue")
                            else:
                                self.colorvals.append("orange")
                        else:
                            self.colorvals.append((1 - m.scale(self.minv, val[0], self.maxv, 0, 1),
                                                   0.5 - m.scale(self.minv, val[0], self.maxv, 0, 0.5),
                                                   m.scale(self.minv, val[0], self.maxv, 0, 1)))

    def graph(self):
        self.plt.set_xlim(-1,1)
        self.plt.set_ylim(-1,1)
        self.plt.set_zlim(-1,1)
        graph.Graph3D(self.xvals, self.yvals, self.zvals, self.colorvals,
                      self.xaxis, self.yaxis, self.zaxis, title = "Classification Edge", plt=self.plt)




def run():
    netfile = 'testnet'
    net = gn.loadNets(netfile)[0][0]

    xaxis = "Embarcked"
    yaxis = "Parch"
    zaxis = "Age"
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    #GraphNet(net, xaxis, yaxis, zaxis, plt)
    g = GraphManager(net, xaxis, yaxis, zaxis, plt)
    g.reduce()
    g.prep()
    g.graph()
    pyplot.show()