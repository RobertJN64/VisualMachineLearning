import TKinterModernThemes as TKMT
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Visual Machine Learning")

        button_frame = ttk.LabelFrame(self, text="Programs", padding=(20, 20))
        button_frame.grid(row=0, column=0, padx=(20, 20), pady=10, sticky="nsew")

        self.ndButton = ttk.Button(button_frame, text="Net Demo", command=netDemo)
        self.ndButton.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.gadButton = ttk.Button(button_frame, text="Genetic Algorithm Demo", command=genetic)
        self.gadButton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.naButton = ttk.Button(button_frame, text="Net Analyzer", command=self.netAnalyzer)
        self.naButton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.run()

    def netAnalyzer(self):
        fname = filedialog.askopenfilename(parent=self, title="Choose a net file.", initialdir=__file__+"/..",
                                           filetypes=[("Net Files", "*.json")])
        if fname is not None:
            fname = fname.strip('.json')
            import NetAnalyzer
            NetAnalyzer.analyze(fname)



def netDemo():
    import NetDemo
    NetDemo.run()

def genetic():
    import GeneticAlgDemo
    GeneticAlgDemo.run()


def old():
    mode = str(input("Net/Genetic/Analyze/Interactive/Report/Template/Graph/Animate/3D: "))

    if mode == "Genetic":
        pass

    elif mode == "Analyze":
        import NetAnalyzer
        net = str(input("File name: "))


    elif mode == "Interactive":
        import InteractiveGrapher
        net = str(input("File name: "))
        InteractiveGrapher.graph(net)

    elif mode == "Report":
        import ReportGenerator as rg
        rg.GenerateReport()

    elif mode == "Template":
        import ReportCreatingAssist as r
        r.run()

    elif mode == "Graph":
        import Graph as g
        import json
        config = json.loads(input("Enter graph command: "))
        g.Graph(config)

    elif mode == "Animate":
        import AnimatedGraphing as ag
        ag.animate()

    elif mode == "3D":
        import Graph3D
        Graph3D.run()

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

    else:
        print("Not a valid mode")

App()