from MachineLearning import GeneticNets as gn
import PythonExtended.Graphing as graph
import TKinterModernThemes as TKMT
import tkinter as tk

class animObject:
    def __init__(self, ax, net, xaxis, yaxis, animaxis):
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.animaxis = animaxis
        self.zaxis = ' & '.join(net.outputs)
        self.xs = []
        self.ys = []
        self.zs = []
        self.cs = []

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
            self.xs.append(xvals)
            self.ys.append(yvals)
            self.zs.append(zvals)
            self.cs.append(colorvals)
            a += 0.1

        maxvs = []
        minvs = []
        for vals in self.zs:
            maxvs.append(max(vals))
            minvs.append(min(vals))
        self.zmax = max(maxvs)
        self.zmin = min(minvs)

        self.ax = ax

    def graph(self, stage):
        self.ax.clear()
        self.ax.set_zlim([self.zmin, self.zmax])
        graph.Graph3D(self.xs[stage], self.ys[stage], self.zs[stage],
                      self.cs[stage], self.xaxis, self.yaxis, self.zaxis,
                      self.animaxis + ": " + str(round(stage,1)), plt=self.ax)

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, net):
        super().__init__("Net File Animation")
        self.net = net

        self.animobject = None

        graphframe = self.addLabelFrame("Graph")
        data = graphframe.matplotlibFrame("Matplotlib Frame", projection='3d')
        self.canvas, fig, self.ax, backgroundcolor, accentcolor = data
        configframe = self.addLabelFrame("Configuration", col=1)

        self.menuoptions = ["Pick an option"] + list(net.inputs.keys())
        self.xaxisvar = tk.StringVar(value=self.menuoptions[0])
        self.yaxisvar = tk.StringVar(value=self.menuoptions[0])
        self.timeaxisvar = tk.StringVar(value=self.menuoptions[0])

        configframe.Label("X axis:")
        configframe.Label("Y axis:")
        configframe.Label("Time axis:")
        configframe.setActiveCol(1)
        configframe.OptionMenu(self.menuoptions, self.xaxisvar, self.updateAxis)
        configframe.OptionMenu(self.menuoptions, self.yaxisvar, self.updateAxis)
        configframe.OptionMenu(self.menuoptions, self.timeaxisvar, self.updateAxis)
        #self.debugPrint()

        configframe.setActiveCol(0)
        self.scrollvar = tk.IntVar(value=11)
        self.scrollvar.trace_add('write', self.updateGraph)
        self.scale = configframe.Scale(0, 20, self.scrollvar, colspan=2)

        self.switchvar = tk.BooleanVar(value=True)
        configframe.SlideSwitch("AutoScroll", self.switchvar)
        self.root.after(250, self.advanceAnimation)
        self.run()

    def updateAxis(self, _):
        for var in [self.xaxisvar, self.yaxisvar, self.timeaxisvar]:
            if var.get() == self.menuoptions[0]:
                break
        else:
            self.animobject = animObject(self.ax, self.net, self.xaxisvar.get(), self.yaxisvar.get(),
                                         self.timeaxisvar.get())
            self.animobject.graph(0)
            self.canvas.draw()

    def updateGraph(self, _, __, ___):
        if self.animobject is not None:
            self.animobject.graph(self.scrollvar.get())
            self.canvas.draw()

    def advanceAnimation(self):
        if self.switchvar.get() and self.animobject is not None:
            self.scrollvar.set((self.scrollvar.get() + 1)%21)
        self.root.after(250, self.advanceAnimation)


def animate(netfile):
    net = gn.loadNets(netfile)[0][0]
    App(net)