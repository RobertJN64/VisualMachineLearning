from MachineLearning import GeneticNets as gn
import matplotlib.pyplot as pyplot
import PythonExtended.Graphing as graph

class animObject:
    def __init__(self, net, xaxis, yaxis, animaxis):
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.animaxis = animaxis
        self.zaxis = ' & '.join(net.outputs)
        self.xs = {}
        self.ys = {}
        self.zs = {}
        self.cs = {}

        a = -1
        while a < 1:
            xvals = []
            yvals = []
            zvals = []
            colorvals = []

            x = -1
            while x <= 1:
                y = -1
                while y <= 1:
                    xvals.append(x)
                    yvals.append(y)

                    net.reset()
                    for inName in net.inputs:
                        if inName == xaxis:
                            net.setNode(inName, x)
                        elif inName == yaxis:
                            net.setNode(inName, y)
                        elif inName == animaxis:
                            net.setNode(inName, a)
                        else:
                            net.setNode(inName, 0)
                    net.process()
                    out = net.getNode(net.classifier_output)
                    if out > 0:
                        colorvals.append("blue")
                    else:
                        colorvals.append("orange")
                    zvals.append(out)

                    y += 0.1
                x += 0.1
                self.xs[a] = xvals
                self.ys[a] = yvals
                self.zs[a] = zvals
                self.cs[a] = colorvals
            a += 0.1

        maxvs = []
        minvs = []
        for stage in self.zs:
            vals = self.zs[stage]
            maxvs.append(max(vals))
            minvs.append(min(vals))
        self.zmax = max(maxvs)
        self.zmin = min(minvs)

        pyplot.ion()
        self.fig = pyplot.figure()
        self.plt = self.fig.add_subplot(111, projection='3d')

        pyplot.show()

    def graph(self, stage):
        pyplot.cla()
        self.plt.set_zlim([self.zmin, self.zmax])
        graph.Graph3D(self.xs[stage], self.ys[stage], self.zs[stage],
                      self.cs[stage], self.xaxis, self.yaxis, self.zaxis,
                      self.animaxis + ": " + str(round(stage,1)), plt=self.plt)
        self.fig.canvas.flush_events()


def animate():
    netfile = 'testnet'
    net = gn.loadNets(netfile)[0][0]

    xaxis = "Fare"
    yaxis = "Parch"
    animaxis = "Age"

    anim = animObject(net, xaxis, yaxis, animaxis)

    animstage = -1


    while True:
        animstage += 0.1
        if animstage > 1:
            animstage = -1

        if pyplot.get_fignums():
            anim.graph(animstage)
        else:
            break