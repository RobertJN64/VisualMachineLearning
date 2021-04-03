import MachineLearning.GeneticNets as gn
import GraphingExt
import PygameExt as pyg
import pygame
from matplotlib import pyplot

import json
from time import sleep
import copy

#order of output colors
colors = [[(255,0,0), 'red'],
          [(0,128,0), 'green'],
          [(255,255,0), 'yellow'],
          [(255,140,0), 'orange']]

colormodes = ['No Colorization', 'Score Colorization', 'Net Colorization']

#TODO scale points better once data is added

class datapoint:
    def __init__(self, x, y, val, count, z=0, classification = 0):
        self.x = x
        self.y = y
        self.z = z
        self.val = val
        self.count = count
        self.classification = classification

def getDataPoint(x,y, xlist, ylist, zlist):
    for index in range(0, len(xlist)):
        x2 = xlist[index]
        y2 = ylist[index]
        if (x2 - 0.05 <= x <= x2 + 0.05 and
            y2 - 0.05 <= y <= y2 + 0.05):
            return zlist[index]
    print("ERROR!")
    print(x, y)
    print(xlist, ylist, zlist)
    return 0

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
    outcolors = []
    for name in outputdict:
        if outputdict[name].state:
            outputs.append(name)
            for color in colors:
                if outputdict[name].clickedColor == color[0]:
                    outcolors.append(color[1])

    #endregion
    #region send data to net
    xs = []
    ys = []
    zs = []
    for name in outputs:
        xvals = []
        yvals = []
        zvals = []
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
                    else:
                        net.setNode(inName, defvalue)
                net.process()
                zvals.append(net.getNode(name))
                y += 0.1
            x += 0.1
        xs.append(xvals)
        ys.append(yvals)
        zs.append(zvals)
    #endregion
    zaxis = ' & '.join(outputs)

    #region handle dataset
    if data is not None and data != {}:
        dataxvals = []
        datayvals = []
        datazvals = []
        datapoints = [] #for clumping
        datasizevals = []#for clumping

        color = []

        if percents:
            datapoints = []
            x = -1
            while x <= 1:
                y = -1
                while y <= 1:
                    datapoints.append(datapoint(x,y,0,0,classification=0))
                    y += 0.1
                x += 0.1
        elif clump:
            datapoints = []

        for item in data["data"]:
            xval = gn.scale(data["inputs"][xaxis]["min"], item[xaxis], data["inputs"][xaxis]["max"], minx=-1, maxx=1)
            yval = gn.scale(data["inputs"][yaxis]["min"], item[yaxis], data["inputs"][yaxis]["max"], minx=-1, maxx=1)
            zval = gn.scale(data["outputs"][outputs[0]]["min"], item[outputs[0]], data["outputs"][outputs[0]]["max"], minx=-1, maxx=1)

            if colormode == 2:
                net.reset()
                indict = copy.deepcopy(item)
                indict.pop(outputs[0])
                net.receiveInput(indict)
                net.process()
                thisval = net.getNode(outputs[0])
                correctval = item[outputs[0]] > 0
            else:
                thisval = zval
                correctval = getDataPoint(xval, yval, xs[0], ys[0], zs[0])
            if colormode > 0:
                if (thisval > 0 and correctval > 0) or (thisval <= 0 and correctval <= 0):
                    colorval = 'blue'
                else:
                    colorval = 'black'
            else:
                colorval = 'blue'

            if percents:
                for index in range(0, len(datapoints)):
                    if datapoints[index].x - 0.05 < xval < datapoints[index].x + 0.05 and datapoints[index].y - 0.05 < yval < datapoints[index].y + 0.05:
                        if zval > 0:
                            datapoints[index].val += zval
                        datapoints[index].count += 1
                        if (thisval > 0 and correctval > 0 ) or (thisval <= 0 and correctval <= 0):
                            datapoints[index].classification += 1
                        else:
                            datapoints[index].classification -= 1

            elif clump:
                found = False
                for point in datapoints:
                    if (point.x - 0.1 <= xval < point.x + 0.1 and
                        point.y - 0.1 <= yval < point.y + 0.1 and
                        point.z - 0.1 <= zval < point.z + 0.1 and
                        ((thisval > 0 and correctval > 0 ) or (thisval <= 0 and correctval <= 0) == point.classification)):
                        point.count += 1
                        found = True
                if not found:
                    datapoints.append(datapoint(round(xval,1), round(yval,1), 0, 1, z=round(zval,1),
                                                classification=(thisval > 0 and correctval > 0 ) or (thisval <= 0 and correctval <= 0)))

            else:
                dataxvals.append(xval)
                datayvals.append(yval)
                datazvals.append(zval)
                color.append(colorval)



        if percents or clump:
            for point in datapoints:
                if point.count > 0:
                    dataxvals.append(point.x)
                    datayvals.append(point.y)
                    datasizevals.append(point.count * 1)
                    if percents:
                        datazvals.append(gn.scale(0, point.val / point.count, 1))
                        correctval = getDataPoint(point.x, point.y, xs[0], ys[0], zs[0])
                        thisval = 2 * (point.val / point.count) - 1

                    elif clump:
                        if point.classification:
                            point.z += 0.1
                        datazvals.append(point.z)
                        correctval = getDataPoint(point.x, point.y, xs[0], ys[0], zs[0])
                        thisval = point.z
                    else:
                        correctval = 0
                        thisval = 0
                    if colormode == 1:
                        if (correctval > 0 and thisval > 0) or (correctval <= 0 and thisval <= 0):
                            color.append('blue')
                        else:
                            color.append('black')
                    elif colormode == 2:
                        if percents:
                            color.append((0,0,gn.scale(-point.count, point.classification, point.count, minx = 0, maxx=1))) #color scale from 0 to 1
                        elif clump:
                            if point.classification:
                                color.append('blue')
                            else:
                                color.append('black')
                    else:
                        color.append('blue')

            GraphingExt.Graph3D(dataxvals, datayvals, datazvals, color, xaxis, yaxis, zaxis, title, plt=fig, s=datasizevals)
        else:
            GraphingExt.Graph3D(dataxvals, datayvals, datazvals, color, xaxis, yaxis, zaxis, title, plt=fig)
        if percents:
            pyplot.gca().set_zlim(-1, 1)

    #endregion handle dataset
    GraphingExt.multiGraph3D(xs,ys,zs, outcolors, xaxis, yaxis, zaxis, title, plt=fig)

def graph(fname):
    net = gn.loadNets(fname)[0][0]

    #region init matplotlib
    pyplot.ion()
    fig = pyplot.figure()
    fig.canvas.set_window_title('Interactive Grapher')
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
                             text=colormodes[colormode], textsize=10, textcolor=(255, 255, 255))
    buttons.addButton(colorButton)

    clumpButton = pyg.Button(450, 205, 100, 25, (50,50,50), toggle=True, clickedColor=(200,200,0),
                             text="Clump", textsize=15, textcolor=(255, 255, 255))
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
                if file is None:
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