import TKinterModernThemes as TKMT
from tkinter import ttk
from tkinter import filedialog

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Visual Machine Learning")

        button_frame = ttk.LabelFrame(self, text="Programs", padding=(20, 20))
        button_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Net Demo", command=netDemo)
        button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Genetic Algorithm Demo", command=genetic)
        button.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Net Analyzer", command=self.netAnalyzer)
        button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Interactive Grapher", command=self.interactiveGrapher)
        button.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Create Report", command=createReport)
        button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Create Report Template", command=createReportTemplate)
        button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Graph Animation", command=animate)
        button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        button = ttk.Button(button_frame, text="Graph 3D", command=graph3D)
        button.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

        self.run()

    def netAnalyzer(self):
        fname = filedialog.askopenfilename(parent=self, title="Choose a net file.", initialdir=__file__+"/..",
                                           filetypes=[("Net Files", "*.json")])
        if fname is not None:
            fname = fname.strip('.json')
            import NetAnalyzer
            NetAnalyzer.analyze(fname)

    def interactiveGrapher(self):
        fname = filedialog.askopenfilename(parent=self, title="Choose a net file.", initialdir=__file__ + "/..",
                                           filetypes=[("Net Files", "*.json")])
        if fname is not None:
            fname = fname.strip('.json')
            import InteractiveGrapher
            InteractiveGrapher.graph(fname)



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

def animate():
    import AnimatedGraphing as ag
    ag.animate()

def graph3D():
    import Graph3D
    Graph3D.run()


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