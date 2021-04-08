import MachineLearning.GeneticNets as gn
import MachineLearning.Graphing as MLGraph
import matplotlib.pyplot as pyplot
import json

def Graph(config):
    netfile = config["net-file"]
    net = gn.loadNets(netfile)[0][0]

    usedata = config["use-data"]

    xaxis = config["xaxis"]
    yaxis = config["yaxis"]
    zaxis = config["zaxis"]

    fig = pyplot.figure()
    plt = fig.add_subplot(111, projection='3d')
    if usedata:
        datafile = config["data-file"]
        colormode = config["color-mode"]
        useclumping = config["clump"]
        usepercents = config["usepercents"]
        with open(datafile) as f:
            data = json.load(f)
        MLGraph.GraphNetData(net, data, xaxis, yaxis, zaxis, 0, useclumping, usepercents, colormode, plt)
    else:
        MLGraph.GraphNet(net, xaxis, yaxis, plt)

    pyplot.show()

