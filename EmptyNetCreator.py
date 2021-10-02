import MachineLearning.GeneticNets as gn
import TKinterModernThemes as TKMT
import tkinter as tk
from tkinter import filedialog


class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Empty Net Creator")
        frame = self.addLabelFrame("Configuration")

        self.innodesvar = tk.IntVar(value=1)
        frame.Text("Number of input nodes: ")
        frame.NumericalSpinbox(1,100,1, self.innodesvar)

        self.outnodesvar = tk.IntVar(value=1)
        frame.Text("Numer of output nodes: ")
        frame.NumericalSpinbox(1,100,1,self.outnodesvar)

        self.widthvar = tk.IntVar(value=1)
        frame.Text("Numer of mid node rows: ")
        frame.NumericalSpinbox(1,100,1, self.widthvar)

        self.depthvar = tk.IntVar(value=1)
        frame.Text("Number of mid nodes per row: ")
        frame.NumericalSpinbox(1,100,1, self.depthvar)

        frame.setActiveCol(1)
        frame.Text(" ")
        frame.setActiveCol(2)
        self.biasvar = tk.BooleanVar()
        frame.SlideSwitch("Use Bias", self.biasvar)

        self.neatvar = tk.BooleanVar()
        frame.SlideSwitch("Use Neat", self.neatvar)

        options = ["old", "sigmoid", "relu"]
        self.actfuncvar = tk.StringVar(value=options[1])
        self.finactfuncvar = tk.StringVar(value=options[1])
        frame.Text("Activation Function:")
        frame.OptionMenu(options, self.actfuncvar, default='sigmoid')
        frame.Text("Final Activation Function:")
        frame.OptionMenu(options, self.finactfuncvar, default='sigmoid')

        frame = self.addFrame("Button Frame")
        frame.AccentButton("Create net!", self.createNet)

    def createNet(self):
        inputs = []
        for i in range(0, self.innodesvar.get()):
            inputs.append("Input" + str(i))
        outputs = []
        for i in range(0, self.outnodesvar.get()):
            outputs.append("Output" + str(i))
        netDB = gn.Random(inputs, outputs, 1, self.widthvar.get(), self.depthvar.get(), bias=self.biasvar.get(),
                          neat=self.neatvar.get(), activation_func=self.actfuncvar.get(),
                          final_activation_func=self.finactfuncvar.get())

        file = filedialog.asksaveasfilename(parent=self.master, title="Save Empty Net",
                                            filetypes = [["Net Files", "*.json"]])
        gn.saveNets([netDB[0][0]], file, "EmptyNet", 1.0)
