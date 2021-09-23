import MachineLearning.GeneticNets as gn
import MachineLearning.Graphing as grapher
import PythonExtended.Pygame as pyg
import pygame
from matplotlib import pyplot

import json
from time import sleep

#order of output colors
colors = grapher.colors
colormodes = ['none', 'data-file', 'score', 'net-score', 'var-error']

def creategraph(fig, net, inputdict, outputdict, title, defvalue=0, data=None, percents=False, colormode=0, clump=False):
    #we can assume that inputs = 2, and outputs > 1:
    #region scan inputs and outputs
    xaxis = ""
    yaxis = ""
    for name in inputdict:
        if inputdict[name].state:
            if xaxis == "":
                xaxis = name
            elif yaxis == "":
                yaxis = name
            else:
                print("Error, too many inputs")

    outputs = []
    for name in outputdict:
        if outputdict[name].state:
            outputs.append(name)

    if data != {} and data is not None:
        grapher.GraphNetData(net, data, xaxis, yaxis, net.classifier_output, defvalue, clump, percents, colormodes[colormode], fig, title=title)
    else:
        grapher.GraphNetOutputs(net, xaxis, yaxis, outputs, fig, title=title)

def graph(fname):
    net = gn.loadNets(fname)[0][0]
    #region init matplotlib
    pyplot.ion()
    fig = pyplot.figure()
    pyplot.get_current_fig_manager().set_window_title("Interactive Grapher")
    fig.show()
    #endregion
    #region init pygame
    pygame.init()
    screen = pyg.createScreen(600, 600, "Interactive Graphing Control Panel", resize=True)
    #endregion
    colormode = 0

    #region add buttons
    buttons = pyg.ButtonManager()
    inputButtonDict = {}
    outputButtonDict = {}
    #region inputs
    x = 50
    y = 125
    button = None
    for name in net.inputs:
        button = pyg.Button(x, y, 100, 25,
                                     (50,50,50), clickedColor=(200,200,0),
                                     text=str(name), textcolor=(255,255,255), textsize=15, toggle=True)
        inputButtonDict[name] = button
        buttons.addButton(button)
        y += 40
    #endregion inputs
    #region outputs
    x = 250
    y = 125
    count = 0
    for name in net.outputs:
        button = pyg.Button(x, y, 100, 25,
                                     (50,50,50), clickedColor=colors[count][0],
                                     text=str(name), textcolor=(255,255,255), textsize=15, toggle=True)
        outputButtonDict[name] = button
        buttons.addButton(button)
        count += 1
        y += 40

    if len(net.outputs) == 1:
        button.state = True
    #endregion outputs

    dataButton = pyg.Button(450, 125, 100, 25, (50,50,50), clickedColor=(200,200,0), toggle=True,
                            text="Add Data", textsize=15, textcolor=(255,255,255))
    buttons.addButton(dataButton)

    percentButton = pyg.Button(450, 165, 100, 25, (50, 50, 50), clickedColor=(200, 200, 0), toggle=True,
                             text='Data Percentages', textsize=10, textcolor=(255, 255, 255))
    buttons.addButton(percentButton)

    colorButton = pyg.Button(450, 245, 100, 25, (50, 50, 50), toggle=False,
                             text=colormodes[colormode], textsize=15, textcolor=(255, 255, 255))
    buttons.addButton(colorButton)

    clumpButton = pyg.Button(450, 205, 100, 25, (50,50,50), toggle=True, clickedColor=(200,200,0),
                             text="Clump", textsize=15, textcolor=(255, 255, 255))
    clumpButton.state = True
    buttons.addButton(clumpButton)

    #endregion add buttons
    #region in out vars
    inputCount = 0
    outputCount = 0
    state = {}
    donextframe = False
    ins = {}
    outs = {}
    #endregion in out vars
    data = {}

    done = False
    while not done:
        #region screen layout
        screen.fill((200, 200, 200))
        pygame.draw.rect(screen, (0,0,0), (25,10,550,50), width=3)
        pygame.draw.rect(screen, (0,0,0), (25, 80, 150, 400), width=3)
        pygame.draw.rect(screen, (0, 0, 0), (225, 80, 150, 400), width=3)
        pygame.draw.rect(screen, (0, 0, 0), (425, 80, 150, 400), width=3)
        pyg.message_display(screen, "3D Grapher", (300,25), (0,0,0), 25)
        pyg.message_display(screen, "Net from file: " + fname, (300,50), (0,0,0), 15)
        pyg.message_display(screen, "Inputs", (100, 100), (0,0,0), 15)
        pyg.message_display(screen, "Outputs", (300, 100), (0, 0, 0), 15)
        pyg.message_display(screen, "Settings", (500,100), (0,0,0), 15)

        if inputCount != 2:
            pyg.message_display(screen, "Select 2 Inputs", (100,500), (0,0,0), 15)
        if outputCount == 0:
            pyg.message_display(screen, "Select Outputs", (300,500), (0,0,0), 15)


        #endregion screen layout

        buttons.draw(screen)
        pygame.display.update()

        #region events
        events = pygame.event.get()
        buttons.resetEvents()
        for event in events:
            buttons.recieveEvent(event)
        #endregion

        #region count ins/outs
        inputCount = 0
        for name in inputButtonDict:
            if inputButtonDict[name].state:
                inputCount += 1

        outputCount = 0
        for name in outputButtonDict:
            if outputButtonDict[name].state:
                outputCount += 1
        #endregion

        #region Graph
        if donextframe:
            plt = fig.add_subplot(111, projection='3d')
            creategraph(plt, net, ins, outs, "Net from file: " + fname, data=data, percents = percentButton.state, colormode = colormode, clump=clumpButton.state)
            donextframe = False

        fig.canvas.flush_events()
        #endregion Graph

        #region check for change
        newstate = buttons.getEvents()

        if newstate != state:
            state = newstate
            pyplot.clf()
            if inputCount == 2 and outputCount > 0:
                donextframe = True
                ins = inputButtonDict
                outs = outputButtonDict
        #endregion

        #region adddata
        if dataButton.updated:
            if dataButton.state:
                file = net.datafile
                if file is None or file == "":
                    file = input("Data source file: ")
                with open(file) as f:
                    data = json.load(f)
            else:
                data = {}
        #endregion

        #region colormode
        if colorButton.updated:
            colormode += 1
            if colormode >= len(colormodes):
                colormode = 0
            colorButton.text = colormodes[colormode]
        #endregion colormode

        #region clump/%
        if clumpButton.updated and clumpButton.state and percentButton.state:
            percentButton.state = False
        if percentButton.updated and clumpButton.state and percentButton.state:
            clumpButton.state = False

        #endregion

        #region exit loop
        if pyg.checkClose(events):
            pygame.quit()
            done = True
        #endregion
        sleep(0.01)