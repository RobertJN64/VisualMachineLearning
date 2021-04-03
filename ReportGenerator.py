import MachineLearning.GeneticNets as gn
import MachineLearning.GeneticEvolution as ge
import PythonExtended.Graphing as graph
import matplotlib.pyplot as pyplot

import json
import warnings
import os
import shutil #temporary for testing
#import datetime #needed after testing

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
    return '<div>\n'

def GenerateDivEnd():
    return '</div>\n'
#endregion

#region generators
def GenerateHeader(config):
    return '<h1>' + config['text'] + '</h1>\n'

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
            out += "<p>Net has no hidden layers."

    return out

def GenerateDataInfo(net, data, config):
    out = "<h3>Training Data Info</h3>\n"
    out += "<p>Data file has " + str(len(data["data"])) + " lines."
    score = ge.Test_Obj(net, data["data"], config["comparison-mode"])
    out += "<p>We correctly predict " + str(round(score * 100 / len(data["data"]),3)) + "% of these.</p>\n"
    return out

#order of output colors
colors = [[(255,0,0), 'red'],
          [(0,128,0), 'green'],
          [(255,255,0), 'yellow'],
          [(255,140,0), 'orange']]
def CustomNetGraph(net, config, directory, fname):
    if config["x"] is None or config["y"] is None:
        warnings.warn("Custom net graph missing configuration")

    xaxis = config["x"]
    yaxis = config["y"]
    zaxis = ' & '.join(net.outputs)
    #region send data to net
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
    #endregion
    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    graph.multiGraph3D(xs, ys, zs, outcolors, xaxis, yaxis, zaxis, xaxis + " by " + yaxis, plt=plt)
    pyplot.savefig(directory + '/' + fname)
    out = "<h3>" + config["header"] + "</h3>\n"
    out += '<img src="' + fname + '"</img>\n'
    return out

def HighVarianceGraph(net, config, directory, fname):
    #region Measure Variance
    best = 0
    secondbest = 0
    xaxis = ""
    yaxis = ""
    for inputa in net.inputs:
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
    #endregion
    return CustomNetGraph(net, {"x": xaxis, "y":yaxis, "header":"High Variance Graph"}, directory, fname)

def HighPredictionGraph(net, config, directory, fname):
    return ""

def GenerateCustomText(config):
    return "<p>" + config["text"] + "</p>\n"

def GenerateCustomHeader(config):
    return "<h3>" + config["text"] + "</h3>\n"

#endregion


def GenerateReport():
    #region load config and template
    with open("ReportSettings/defconfig.json") as f:
        defconfig = json.load(f)

    with open("ReportSettings/config.json") as f:
        custconfig = json.load(f)

    with open("ReportSettings/template.txt") as f:
        template = f.readlines()

    for i in range(0, len(template)):
        template[i] = template[i].strip('\n')
    #endregion
    #region assert config structure
    if "net-file" not in custconfig:
        warnings.warn("Config file missing net file name")
        return

    if "use-data" in custconfig and "data-file" not in custconfig:
        warnings.warn("Config file asks to use data, but no data file specified")
        return
    #endregion
    #region load net + data
    net = gn.loadNets(custconfig["net-file"])[0][0]
    data = None
    if custconfig["use-data"]:
        with open(custconfig["data-file"]) as f:
            data = json.load(f)
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
    file += GenerateStart()

    linenumber = 0
    for line in template:
        #region Line + Info
        line = line.split(' | ')
        info = {}
        if len(line) == 0:
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
            if key in localconfig:
                localconfig[key] = custconfig[key]
            else:
                pass #we can ignore some keys here

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
        elif line == "custom-net-graph":
            file += CustomNetGraph(net, localconfig, fname, str(linenumber)+"img.png")
        elif line == "custom-text":
            file += GenerateCustomText(localconfig)
        elif line == "custom-header":
            file += GenerateCustomHeader(localconfig)
        elif line == "high-variance-graph":
            file += HighVarianceGraph(net, localconfig, fname, str(linenumber)+"img.png")
        elif line == "high-prediction-graph":
            file += HighPredictionGraph(net, localconfig, fname, str(linenumber)+"img.png")

        else:
            warnings.warn("ReportGenerator is missing function " + line)
        file += GenerateDivEnd()

        linenumber += 1

    file += GenerateEnd()

    #region export
    with open(fname + "/report.html", "w") as f:
        f.write(file)
    #endregion
