import TKinterModernThemes as TKMT
from tkinter import filedialog

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Visual Machine Learning")
        programs = [["Net Demo", netDemo], ["Genetic Algorithm Demo", genetic], ["Net Analyzer", self.netAnalyzer],
                    ["Interactive Grapher", self.interactiveGrapher], ["Create Report", createReport],
                    ["Create Report Template", createReportTemplate], ["Graph Animation", self.animatedGrapher],
                    ["Graph 3D", graph3D]]

        button_frame = self.addLabelFrame("Programs")
        for name, program in programs:
            button_frame.Button(name, program)

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
            NetAnalyzer.analyze(fname)

    def interactiveGrapher(self):
        fname = self.openFile("Choose a net file")
        if fname is not None:
            import InteractiveGrapher
            InteractiveGrapher.graph(fname)

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
    r.run()

def graph3D():
    import Graph3D
    Graph3D.run()
#endregion

def old():
    mode = str(input("Net/Genetic/Analyze/Interactive/Report/Template/Graph/Animate/3D: "))

    if mode == "Genetic":
        pass


    elif mode == "Graph":
        import Graph as g
        import json
        config = json.loads(input("Enter graph command: "))
        g.Graph(config)


    elif mode == "CreateEmptyNet":
        #Saves an empty net to a file
        import EmptyNetCreator
        file = str(input("Enter ouput file name: "))
        inputLen = int(input("Number of input nodes: "))
        outputLen = int(input("Number of output nodes: "))
        midWidth = int(input("Number of mid node rows: "))
        midDepth = int(input("Number of mid nodes per row: "))

        useBias = str(input("Use bias? "))
        if useBias == "" or useBias == "True":
            useBias = True
        else:
            useBias = False

        useNeat = str(input("Use neat? "))
        if useNeat == "" or useNeat == "False":
            useNeat = False
        else:
            useNeat = True

        activation_func = str(input("Activation function? "))
        if activation_func == "":
            activation_func = "old"

        if activation_func not in ["old", "sigmoid", "relu"]:
            print("ERROR! Activation function not found")

        fin_activation_func = str(input("Final activation function? "))
        if fin_activation_func == "":
            fin_activation_func = "old"

        if fin_activation_func not in ["old", "sigmoid", "relu"]:
            print("ERROR! Activation function not found")

        EmptyNetCreator.create(file, inputLen, outputLen, midWidth, midDepth, useBias, useNeat, activation_func, fin_activation_func)


App()