import TKinterModernThemes as TKMT
from tkinter import filedialog
import math

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Visual Machine Learning")
        programs = [["Net Demo", netDemo], ["Genetic Algorithm Demo", genetic], ["Net Analyzer", self.netAnalyzer],
                    ["Interactive Grapher", self.interactiveGrapher], ["Create Report", createReport],
                    ["Create Report Template", createReportTemplate], ["Graph Animation", self.animatedGrapher],
                    ["Graph 3D", graph3D], ["Empty Net Creator", emptyNetCreator]]

        button_frame = self.addLabelFrame("Programs")
        for i in range(0, len(programs)):
            name, program = programs[i]
            button_frame.Button(name, program, col=math.ceil((i+1)*2/(len(programs)+1)))

        self.run()

    def openFile(self, title, filetypes=None):
        if filetypes is None:
            filetypes = [("Net Files", "*.json")]
        fname = filedialog.askopenfilename(parent=self.master, title=title, initialdir=__file__ + "/..", filetypes=filetypes)
        if fname is not None:
            fname = fname.strip('.json')
        return fname


    def netAnalyzer(self):
        fname = self.openFile("Choose a net file")
        if fname is not None:
            import NetAnalyzer
            NetAnalyzer.analyze(fname) #TODO

    def interactiveGrapher(self):
        fname = self.openFile("Choose a net file")
        if fname is not None:
            import InteractiveGrapher
            InteractiveGrapher.graph(fname) #TODO

    def animatedGrapher(self):
        fname = self.openFile("Choose a net file")
        if fname is not None:
            import AnimatedGraphing as ag
            ag.animate(fname)


#region new launchers
def netDemo():
    import NetDemo
    NetDemo.run()

def genetic():
    import GeneticAlgDemo
    GeneticAlgDemo.run()

def createReport():
    import ReportGenerator as rg
    rg.GenerateReport()

def createReportTemplate():
    import ReportCreatingAssist as r
    r.run() #TODO

def graph3D():
    import Graph3D
    Graph3D.run() #TODO

def emptyNetCreator():
    import EmptyNetCreator
    EmptyNetCreator.App()
#endregion

def old():
    mode = str(input("Net/Genetic/Analyze/Interactive/Report/Template/Graph/Animate/3D: "))

    if mode == "Graph":
        import Graph as g
        import json
        config = json.loads(input("Enter graph command: "))
        g.Graph(config)

App()