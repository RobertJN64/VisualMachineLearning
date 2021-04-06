import MachineLearning.GeneticNets as gn
import MachineLearning.GeneticEvolution as ge
import PythonExtended.Graphing as graph
#import PythonExtended.DataStructures as d
import PythonExtended.Math as m
import matplotlib.pyplot as pyplot

import json
import warnings
import os
import shutil #temporary for testing
#import datetime #needed after testing
import time

# region GLOBAL VARS + classes
class ReportInfo:
    def __init__(self):
        self.totalaccuracy = None
        self.usedvariance = []
        self.usedpredictability = []
        self.nonlinear = []

class datapoint:
    def __init__(self, x, y, z, color=None):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.size = 1

    def isClose(self, dp, useColor=True, xdif=0.1, ydif=0.1, zdif=0.1):
        return (abs(self.x - dp.x) < xdif and
                abs(self.y - dp.y) < ydif and
                abs(self.z - dp.z) < zdif and
                (self.color == dp.color or not useColor))

class graphpoint:
    def __init__(self, x, y, z, color="blue"):
        self.x = x
        self.y = y
        self.z = z

        self.color = color
        self.posicount = z
        self.count = 1

#endregion
#region data management functions
#order of output colors
colors = [[(255,0,0), 'red'],
          [(0,128,0), 'green'],
          [(255,255,0), 'yellow'],
          [(0,0,0), 'black']]

def clump(points, xdif, ydif, zdif, percent=False):
    outpoints = []
    for pointa in points:
        found = False
        for pointb in outpoints:
            if (abs(pointa.x - pointb.x) < xdif and
                abs(pointa.y - pointb.y) < ydif and
                (abs(pointa.z - pointb.z) < zdif or percent)):
                found = True
                pointb.count += 1
                pointb.posicount += pointa.z
        if not found:
            outpoints.append(graphpoint(pointa.x, pointa.y, pointa.z, pointa.color))
    return outpoints

def colorize(points, colormode, percents):
    for point in points:
        if percents:
            point.z = (point.posicount / point.count) * 100
        if colormode == "none":
            point.color = "blue"
        elif colormode == "data-file":
            if percents:
                point.color = (1 - m.scale(0, point.z, 100, 0, 1),
                               0.5 - m.scale(0, point.z, 100, 0, 0.5),
                               m.scale(0, point.z, 100, 0, 1))
            else:
                if point.z > 0:
                    point.color = "blue"
                else:
                    point.color = "orange"
        elif colormode == "score":
            # TODO - score coloring
            pass
        elif colormode == "net-score":
            # TODO - net coloring
            pass
        else:
            warnings.warn("Color mode not found: " + str(colormode))

def colorinfotext(colormode, percents):
    out = ""
    if colormode == "data-file":
        out += '<p>Color mode is based on point output in data file. Blue is 1, orange is 0.</p>\n'
    elif colormode == "score":
        out += '<p>Color mode is based on point value vs net output given those input variables. Blue is 1, orange is 0.</p>\n'
    elif colormode == "net-score":
        out += '<p>Color mode is based on true net score given that point. Blue is 1, orange is 0.</p>\n'
    if percents:
        out += '<p>Data points are clumped into percents.'
    return out
#endregion

#region GraphingFuncs
def GraphNet(net, xaxis, yaxis, fig):
    zaxis = ' & '.join(net.outputs)
    xs = []
    ys = []
    zs = []
    outcolors = []
    count = 0
    for name in net.outputs:
        xvals = []
        yvals = []
        zvals = []
        outcolors.append(colors[count][1])
        count += 1
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
                        net.setNode(inName, 0)
                net.process()
                zvals.append(net.getNode(name))
                y += 0.1
            x += 0.1
        xs.append(xvals)
        ys.append(yvals)
        zs.append(zvals)
    graph.multiGraph3D(xs, ys, zs, outcolors, xaxis, yaxis, zaxis, xaxis + " by " + yaxis, plt=fig)

def GraphNetData(net, data, xaxis, yaxis, zaxis, defvalue, useclump, usepercents, colormode, fig):
    #region handle net
    netxvals = []
    netyvals = []
    netzvals = []

    xmin = data["inputs"][xaxis]["min"]
    xmax = data["inputs"][xaxis]["max"]
    ymin = data["inputs"][yaxis]["min"]
    ymax = data["inputs"][yaxis]["max"]
    zmin = data["outputs"][zaxis]["min"]
    zmax = data["outputs"][zaxis]["max"]

    x = -1
    while x <= 1:
        y = -1
        while y <= 1:
            netxvals.append(m.scale(-1, x, 1, xmin, xmax))
            netyvals.append(m.scale(-1, y, 1, ymin, ymax))
            net.reset()
            for inName in net.inputs:
                if inName == xaxis:
                    net.setNode(inName, x)
                elif inName == yaxis:
                    net.setNode(inName, y)
                else:
                    net.setNode(inName, defvalue)
            net.process()
            if usepercents:
                netzvals.append(m.scale(-1, net.getNode(zaxis), 1, 0, 100))
            else:
                netzvals.append(m.scale(-1, net.getNode(zaxis), 1, zmin, zmax))

            y += 0.1
        x += 0.1
    #endregion
    #region handle data
    datapoints = []
    for item in data["data"]:
        datapoints.append(graphpoint(item[xaxis], item[yaxis], item[zaxis]))

    if useclump or usepercents:
        datapoints = clump(datapoints, (xmax-xmin)/20, (ymax-ymin)/20, (zmax-zmin)/20, usepercents)

    colorize(datapoints, colormode, usepercents)

    dataxvals = []
    datayvals = []
    datazvals = []
    datacolorvals = []
    datasizevals = []
    for point in datapoints:
        dataxvals.append(point.x)
        datayvals.append(point.y)
        datazvals.append(point.z)
        datacolorvals.append(point.color)
        datasizevals.append(point.count)

    size = None
    if useclump or usepercents:
        size = datasizevals

    if usepercents:
        zaxis += "%"

    #endregion
    graph.Graph3D(netxvals,netyvals,netzvals,"red", xaxis, yaxis, zaxis, xaxis + " by " + yaxis, plt=fig)
    graph.Graph3D(dataxvals, datayvals, datazvals, datacolorvals, xaxis, yaxis, zaxis, xaxis + " by " + yaxis, plt=fig, s=size)

def GraphData3Axis(data, xaxis, yaxis, zaxis, coloraxis, useclump, fig):
    xvals = []
    yvals = []
    zvals = []
    svals = []
    colorvals = []
    xvariance = (data["inputs"][xaxis]["max"] - data["inputs"][xaxis]["min"]) / 20
    yvariance = (data["inputs"][yaxis]["max"] - data["inputs"][yaxis]["min"]) / 20
    zvariance = (data["inputs"][zaxis]["max"] - data["inputs"][zaxis]["min"]) / 20
    datapoints = []
    for line in data["data"]:
        pointa = datapoint(line[xaxis], line[yaxis], line[zaxis], line[coloraxis])
        found = False
        for pointb in datapoints:
            if pointa.isClose(pointb, True, xvariance, yvariance, zvariance):
                found = True
                pointb.size += 1
        if not found or not useclump:
            datapoints.append(pointa)

    for point in datapoints:
        xvals.append(point.x)
        yvals.append(point.y)
        zvals.append(point.z)
        svals.append(point.size)
        if point.color > 0:
            colorvals.append("blue")
        else:
            colorvals.append("orange")

    if not useclump:
        svals = None

    graph.Graph3D(xvals, yvals, zvals, colorvals, xaxis, yaxis, zaxis, xaxis + " by " + yaxis + " by " + zaxis, plt=fig,s=svals)

#endregion

#region simple generators
def GenerateStart(title="MachineLearning Report"):
    return ('<!DOCTYPE html>\n' +
            '<html lang="en">\n' +
            '<head>\n' +
            '<meta charset="UTF-8">\n' +
            '<title>' + title + '</title>\n'
            '</head>\n'
            '<body>\n')

def GenerateEnd():
    return ('</body>\n' +
            '</html>\n')

def GenerateDivStart():
    return '<div style="border: 2px;border-color: black;border-radius: 5px;border-style: solid; padding-left: 10px; margin-bottom: 5px">\n'

def GenerateDivEnd():
    return '</div>\n'

def GenerateHeader(config):
    return '<h1>' + config['text'] + '</h1>\n'

def GenerateCustomText(config):
    return "<p>" + config["text"] + "</p>\n"

def GenerateCustomHeader(config):
    return "<h3>" + config["text"] + "</h3>\n"
#endregion

#region generators
def GenerateInfo(net, config):
    out = '<h3>Net Info</h3>\n'
    if config["inputs"]:
        out += "<p>Net has " + str(len(net.inputs)) + " inputs.</p>\n"
    if config["list-inputs"]:
        out += "<ul>\n"
        for name in net.inputs:
            out += "<li>" + name + "</li>\n"
        out += "</ul>\n"
    if config["outputs"]:
        out += "<p>Net has " + str(len(net.outputs)) + " outputs.</p>\n"
    if config["list-outputs"]:
        out += "<ul>\n"
        for name in net.outputs:
            out += "<li>" + name + "</li>\n"
        out += "</ul>\n"
    if config["hidden-layers"]:
        if len(net.midnodes) > 0:
            out += "<p>Net is " + str(len(net.midnodes)) + " wide by " + str(len(net.midnodes[0])) + " deep.</p>\n"
        else:
            out += "<p>Net has no hidden layers.</p>\n"

    layerstr = ""
    if config["individual-layers"]:
        for layer in net.midnodes:
            layerstr += str(len(layer)) + ", "
        layerstr = layerstr[:-2]
        out += "<p>Net hidden layers: " + layerstr + ".</p>\n"
    return out

def GenerateDataInfo(net, data, config):
    global reportinfo
    out = "<h3>Training Data Info</h3>\n"
    out += "<p>Data file has " + str(len(data["data"])) + " lines."
    if reportinfo.totalaccuracy is None:
        reportinfo.totalaccuracy = ge.Test_Obj(net, data["data"], config["comparison-mode"])* 100 / len(data["data"])
    out += "<p>We correctly predict " + str(round(reportinfo.totalaccuracy,3)) + "% of these.</p>\n"
    return out

def GenerateDataPredictionGraph(data, outaxis, config, directory, fname):
    inputs = []
    avgs = []
    count = []

    for item in data["inputs"]:
        inputs.append(item)
        avgs.append([0.0,0.0])
        count.append([0,0])

    for row in data["data"]:
        for i in range(0, len(inputs)):
            for item in inputs:
                if row[outaxis] > 0:
                    avgs[i][1] += row[item]
                    count[i][1] += 1
                else:
                    avgs[i][0] += row[item]
                    count[i][0] += 1

    for i in range(0, len(inputs)):
        avgs[i][0] = avgs[i][0] / count[i][0]
        avgs[i][1] = avgs[i][1] / count[i][1]

    difs = []
    for i in range(0, len(inputs)):
        difs.append(abs(avgs[i][0] - avgs[i][1]) / abs((avgs[i][0] + avgs[i][1])))

    xaxis = ""
    yaxis = ""
    zaxis = ""
    best = 0
    secondbest = 0
    thirdbest = 0
    for i in range(0, len(inputs)):
        dif = difs[i]
        if dif > best:
            zaxis = yaxis
            yaxis = xaxis
            xaxis = inputs[i]
            thirdbest = secondbest
            secondbest = best
            best = dif
        elif dif > secondbest:
            zaxis = yaxis
            yaxis = inputs[i]
            thirdbest = secondbest
            secondbest = dif
        elif dif > thirdbest:
            zaxis = inputs[i]
            thirdbest = dif
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    GraphData3Axis(data, xaxis, yaxis, zaxis, outaxis, config["clump"], plt)
    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    out += colorinfotext("data-file", False)
    return out

def GenerateCustomNetGraph(net, config, directory, fname):
    if config["x"] is None or config["y"] is None:
        warnings.warn("Custom net graph missing configuration")
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    GraphNet(net, config["x"], config["y"], plt)
    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches = 'tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    return out

def GenerateCustomNetDataGraph(net, data, config, directory, fname):
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    GraphNetData(net, data, config["x"], config["y"], list(net.outputs.keys())[0], 0, config["clump"], config["percents"], config["color"], plt)
    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    out += colorinfotext(config["color"], config["percents"])
    return out

def GenerateDataGraph3Axis(data, config, directory, fname):
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    GraphData3Axis(data, config["x"], config["y"], config["z"], config["out"], config["clump"], plt)
    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    return out

def GenerateHighVarianceGraph(net, data, config, directory, fname):
    global reportinfo
    #region Measure Variance
    best = 0
    secondbest = 0
    xaxis = ""
    yaxis = ""
    for inputa in net.inputs:
        if inputa in reportinfo.usedvariance:
            continue
        outputs = []
        x = -1
        while x <= 1:
            net.reset()
            for name in net.inputs:
                if name == inputa:
                    net.setNode(name, x)
                else:
                    net.setNode(name, 0)
            net.process()
            outputs.append(net.getOutput()[list(net.outputs.keys())[0]])
            x += 0.1
        dif = max(outputs) - min(outputs)
        if dif > best:
            yaxis = xaxis
            xaxis = inputa
            secondbest = best
            best = dif
        elif dif > secondbest:
            yaxis = inputa
            secondbest = dif
    if yaxis == "":
        return "<p>Not enough variables to create graph.</p>\n"
    #endregion
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    if not config["add-data"]:
        GraphNet(net, xaxis, yaxis, plt)
    else:
        GraphNetData(net, data, xaxis, yaxis, list(net.outputs.keys())[0], 0, config["clump"], config["percents"], config["color"], plt)
    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    if config["add-data"]:
        out += colorinfotext(config["color"], config["percents"])
    if len(reportinfo.usedvariance) > 0:
        out += "<p>Ignored variables: " + ', '.join(reportinfo.usedvariance) + "</p>\n"
    reportinfo.usedvariance.append(xaxis)
    reportinfo.usedvariance.append(yaxis)
    return out

def GenerateHighPredictionGraph(net, data, config, directory, fname):
    global reportinfo
    # region Measure Prediction
    best = 0
    secondbest = 0
    xaxis = ""
    yaxis = ""
    for inputa in net.inputs:
        if inputa in reportinfo.usedpredictability:
            continue
        score = 0
        for item in data["data"]:
            net.reset()
            for key in item:
                if key == inputa:
                    net.setNode(key, m.unitscale(data["inputs"][key]["min"], item[key], data["inputs"][key]["max"]))
                elif key in net.inputs:
                    net.setNode(key, 0)
            net.process()
            for out in net.outputs:
                val = item[out]
                if config["test-mode"] != "SimplePosi":
                    val = net.scale(out, item[out])
                score += ge.Test_Output(net.getOutput()[out], val, config["test-mode"])

        if score > best:
            yaxis = xaxis
            xaxis = inputa
            secondbest = best
            best = score
        elif score > secondbest:
            yaxis = inputa
            secondbest = score

    if yaxis == "":
        return "<p>Not enough variables for graph.</p>"
    # endregion
    #region Handle graph
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')

    if not config["add-data"]:
        GraphNet(net, xaxis, yaxis, plt)
    else:
        GraphNetData(net, data, xaxis, yaxis, list(net.outputs.keys())[0], 0, config["clump"], config["percents"], config["color"], plt)

    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    if reportinfo.totalaccuracy is None:
        reportinfo.totalaccuracy = ge.Test_Obj(net, data["data"], config["comparison-mode"]) * 100 /len(data["data"])
    localscore = best*100 / len(data["data"])
    out += ("<p>This gets " + str(round(localscore,2)) + "% of the data items correct." +
            "This is " + str(round(localscore*100/reportinfo.totalaccuracy,2)) + "% of the max accuracy.</p>\n")
    #endregion
    if config["add-data"]:
        out += colorinfotext(config["color"], config["percents"])
    if len(reportinfo.usedpredictability) > 0:
        out += "<p>Ignored variables: " + ', '.join(reportinfo.usedpredictability) + "</p>\n"
    reportinfo.usedpredictability.append(xaxis)
    reportinfo.usedpredictability.append(yaxis)
    return out

def GenerateNonLinearVarianceGraph(net, data, config, directory, fname):
    #region measure variance
    variance = []
    nonlinear = []
    inputs = []
    for inputa in net.inputs:
        if inputa in reportinfo.nonlinear:
            continue
        outputs = []
        x = -1
        while x <= 1:
            net.reset()
            for name in net.inputs:
                if name == inputa:
                    net.setNode(name, x)
                else:
                    net.setNode(name, 0)
            net.process()
            outputs.append(net.getOutput()[list(net.outputs.keys())[0]])
            x += 0.1
        variance.append(max(outputs)-min(outputs))
        inputs.append(inputa)
        nonlinear.append((3 < outputs.index(max(outputs)) < 18 or 3 < outputs.index(min(outputs)) < 18))
    #endregion
    #region find nonlinear
    count = 0
    for item in nonlinear:
        if item:
            count += 1
    target = 0
    secondtarget = 0
    xaxis = ""
    yaxis = ""
    bonustext = ""
    if count == 0:
        return "<h3>Non-Linear Variance Graph</h3>\n<p>None found (excluding: " + ', '.join(reportinfo.nonlinear) +")</p>\n"

    if count == 2:
        for i in range(0, len(nonlinear)):
            if nonlinear[i] and xaxis == "":
                xaxis = inputs[i]
            else:
                yaxis = inputs[i]

    if count > 2:
        for i in range(0, len(nonlinear)):
            if nonlinear[i]:
                if variance[i] > target:
                    yaxis = xaxis
                    secondtarget = target
                    xaxis = inputs[i]
                    target = variance[i]
                elif variance[i] > secondtarget:
                    yaxis = inputs[i]
                    secondtarget = variance[i]
        bonustext = "<p>More than 2 non-linear inputs. We picked the ones with the most variance</p>\n"

    if count == 1:
        secondtarget = max(variance)
        for i in range(0, len(nonlinear)):
            if nonlinear[i]:
                xaxis = inputs[i]
                target = variance[i]
        for i in range(0, len(nonlinear)):
            if inputs[i] != xaxis and abs(variance[i] - target) < secondtarget:
                secondtarget = abs(variance[i] - target)
                yaxis = inputs[i]
        bonustext= "<p>Only one non-linear input (" + xaxis +"). We picked a second input with similar variance.</p>\n"
    #endregion

    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    if not config["add-data"]:
        GraphNet(net, xaxis, yaxis, plt)
    else:
        GraphNetData(net, data, xaxis, yaxis, list(net.outputs.keys())[0], 0, config["clump"], config["percents"], config["color"], plt)

    if config["customize"]:
        pyplot.show()
    fig.savefig(directory + '/' + fname, bbox_inches='tight')
    pyplot.close(fig)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    if config["add-data"]:
        out += colorinfotext(config["color"], config["percents"])
    if len(reportinfo.nonlinear) > 0:
        out += "<p>Ignored variables: " + ', '.join(reportinfo.nonlinear) + "</p>\n"
    reportinfo.nonlinear.append(xaxis)
    reportinfo.nonlinear.append(yaxis)
    return out + bonustext

#endregion

reportinfo = ReportInfo()
def GenerateReport():
    global reportinfo
    reportinfo = ReportInfo()
    #region load config and template
    with open("ReportSettings/defconfig.json") as f:
        defconfig = json.load(f)

    with open("ReportSettings/config.json") as f:
        custconfig = json.load(f)

    #endregion
    #region assert config structure
    if "template" not in custconfig:
        warnings.warn("Config file missing template")
        return
    if "net-file" not in custconfig:
        warnings.warn("Config file missing net file name")
        return

    if "use-data" in custconfig and "data-file" not in custconfig:
        warnings.warn("Config file asks to use data, but no data file specified")
        return
    #endregion
    #region load net + data + template
    net = gn.loadNets(custconfig["net-file"])[0][0]
    data = None
    if custconfig["use-data"]:
        with open(custconfig["data-file"]) as f:
            data = json.load(f)

    with open(custconfig["template"]) as f:
        template = f.readlines()

    for i in range(0, len(template)):
        template[i] = template[i].strip('\n')
    #endregion

    #region manage directories
    file = ""
    #fname = "Report " + str(datetime.datetime.now().strftime("%d-%m-%Y %I-%M"))
    fname = "Report"
    if os.path.isdir(fname):
        shutil.rmtree(fname)
    os.mkdir(fname)
    #endregion

    #create report
    starttime = time.time()
    file += GenerateStart()

    linenumber = 0
    for line in template:
        lasttime = time.time()
        #region Line + Info
        line = line.split(' | ')
        info = {}
        if line[0][0] == "#":
            continue
        if len(line) == 0 or line[0] == "":
            warnings.warn("Line " + str(linenumber) + " empty")
            continue

        elif len(line) == 1:
            line = line[0].lower()

        elif len(line) == 2:
            info = json.loads(line[1])
            line = line[0].lower()

        elif len(line) > 2:
            warnings.warn("Line " + str(linenumber) + " has too many items!")
            return

        #endregion
        #region build up input dictionary
        if line not in defconfig:
            warnings.warn("Line " + str(linenumber) + " " + line + " not in defconfig")
            return

        localconfig = defconfig[line]
        for key in custconfig:
            if key in localconfig and custconfig[key] != "default":
                localconfig[key] = custconfig[key]
            else:
                pass #we can ignore some keys here

        if not custconfig["use-data"] and "add-data" in localconfig:
            localconfig["add-data"] = False

        if not custconfig["use-data"] and "requires-data" in localconfig and localconfig["requires-data"]:
            warnings.warn("Adding line <" + line + "> which requires data, but no data provided.")
            return

        for key in info:
            if key in localconfig:
                localconfig[key] = info[key]
            else:
                #this is a problem, a user specified an unexpected key
                warnings.warn("Unexpected key: " + key + " in line " + str(linenumber))

        #endregion

        file += GenerateDivStart()
        if line == "header":
            file += GenerateHeader(localconfig)
        elif line == "info":
            file += GenerateInfo(net, localconfig)
        elif line == "data":
            file += GenerateDataInfo(net, data, localconfig)
        elif line == "data-predictability-graph":
            file += GenerateDataPredictionGraph(data, list(net.outputs.keys())[0], localconfig, fname, str(linenumber)+"img.png")
        elif line == "custom-net-graph":
            file += GenerateCustomNetGraph(net, localconfig, fname, str(linenumber)+"img.png")
        elif line == "custom-net-data-graph":
            file += GenerateCustomNetDataGraph(net, data, localconfig, fname, str(linenumber)+"img.png")
        elif line == "custom-text":
            file += GenerateCustomText(localconfig)
        elif line == "custom-header":
            file += GenerateCustomHeader(localconfig)
        elif line == "high-variance-graph":
            file += GenerateHighVarianceGraph(net, data, localconfig, fname, str(linenumber)+"img.png")
        elif line == "high-prediction-graph":
            file += GenerateHighPredictionGraph(net, data, localconfig, fname, str(linenumber)+"img.png")
        elif line == "nonlinear-variance-graph":
            file += GenerateNonLinearVarianceGraph(net, data, localconfig, fname, str(linenumber)+"img.png")
        elif line == "custom-data-graph":
            file += GenerateDataGraph3Axis(data, localconfig, fname, str(linenumber)+"img.png")

        else:
            warnings.warn("ReportGenerator is missing function " + line)
        file += GenerateDivEnd()

        print("Finished line (" + str(linenumber) + "): " + line + " in " + str(round(time.time() - lasttime, 3)) + " seconds.")

        linenumber += 1

    file += GenerateEnd()

    #region export
    with open(fname + "/report.html", "w") as f:
        f.write(file)
    print("Finished report in " + str(round(time.time() - starttime, 3)) + " seconds.")
    #endregion
