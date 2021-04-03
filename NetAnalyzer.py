import MachineLearning.GeneticNets as gn
from matplotlib import pyplot
import json


out = []
def pprint(string):
    global out
    out.append(string + '\n')
    print(string)

def getDif(a, b):
    output = {}
    for key in a:
        output[key] = b[key]-a[key]
    return output

def getAxis(inputs, skip=None):
    if skip is None:
        skip = []
    answer = None
    if len(inputs) == 1:
        return list(inputs.keys())[0]
    else:
        while answer not in inputs or answer in skip:
            answer = input(str(list(inputs.keys())) + ": ")
        return answer



def analyze(fname, fnameout = None):
    net = gn.loadNets(fname)[0][0]

    pprint("Found net with inputs" + str(list(net.inputs.keys())))
    pprint("Found net with outputs" + str(list(net.outputs.keys())))

    if len(net.midnodes) > 0 and len(net.midnodes[0]) > 0:
        pprint("Hidden layers are " + str(len(net.midnodes)) + " by " + str(len(net.midnodes[0])))

    pprint("\n")

    net.reset()
    for name in net.inputs:
        net.setNode(name, 0)

    net.process()
    defoutputs = net.getOutput()

    mode = input("Run def analysis (y/n): ")
    if mode == "y":
        pprint("Default outputs: " + str(defoutputs))

        net.reset()
        for name in net.inputs:
            net.setNode(name, 1)

        net.process()
        outputs = net.getOutput()

        pprint("All max outputs: " + str(outputs))

        net.reset()
        for name in net.inputs:
            net.setNode(name, -1)

        net.process()
        outputs = net.getOutput()

        pprint("All min outputs: " + str(outputs))

        pprint("\n")

        for name in net.inputs:
            net.reset()
            for name2 in net.inputs:
                if name == name2:
                    net.setNode(name2, -1)
                else:
                    net.setNode(name2, 0)
            net.process()
            output = net.getOutput()
            pprint("When " + str(name) + " is low, outputs change: " + str(getDif(defoutputs, output)))

            net.reset()
            for name2 in net.inputs:
                if name == name2:
                    net.setNode(name2, 1)
                else:
                    net.setNode(name2, 0)
            net.process()
            output = net.getOutput()
            print(output)
            pprint("When " + str(name) + " is high, outputs change: " + str(getDif(defoutputs, output)))
            pprint("")



        if fnameout is None:
            fnameout = fname+'-info.txt'
        with open(fnameout, 'w') as f:
            f.writelines(out)

    print("Interactive mode: ")
    data = []
    datainputs = {}
    dataoutputs = {}
    adddata = str(input("Add data? y/n: "))
    if adddata == "y":
        datafname = str(input("Fname: "))
        with open(datafname) as f:
            data = json.load(f)
        datainputs = data["inputs"]
        dataoutputs = data["outputs"]
        data = data["data"]

    while True:
        mode = str(input("2D/3D: "))

        if mode == "":
            break
        elif mode == "2D":
            print("X Axis:")
            xaxis = getAxis(net.inputs)

            print("Z Axis")
            zaxis = getAxis(net.outputs)

            defvals = float(input("Default value?: "))
            xvals = []

            zvals = []

            x = -1
            while x <= 1:
                xvals.append(x)

                net.reset()
                for name in net.inputs:
                    if name == xaxis:
                        net.setNode(name, x)

                    else:
                        net.setNode(name, defvals)
                net.process()
                zvals.append(net.getNode(zaxis))

                x += 0.1

            # region ADD DATA
            dataxvals = []

            datazvals = []

            if adddata == "y":
                for item in data:
                    net.reset()
                    xval = gn.scale(datainputs[xaxis]["min"], item[xaxis], datainputs[xaxis]["max"], minx=-1, maxx=1)
                    zval = gn.scale(dataoutputs[zaxis]["min"], item[zaxis], dataoutputs[zaxis]["max"], minx=-1, maxx=1)
                    dataxvals.append(xval)
                    datazvals.append(zval)
            # endregion ADD DATA

            fig = pyplot.figure()
            plt = fig.add_subplot(111)
            plt.scatter(xvals, zvals, color="red")
            if adddata == "y":
                plt.scatter(dataxvals, datazvals, color="blue")
            plt.set_xlabel(xaxis)
            plt.set_ylabel(zaxis)
            plt.set_title("Data from net: " + fname)
            pyplot.show()

        elif mode == "3D":

            print("X Axis:")
            xaxis = getAxis(net.inputs)
            print("Y Axis:")
            yaxis = getAxis(net.inputs, skip=[xaxis])

            fig = pyplot.figure()
            plt = fig.add_subplot(111, projection='3d')

            zaxisstr = ""

            done = False
            while not done:
                print("Z Axis")
                zaxis = getAxis(net.outputs, zaxisstr)
                color = str(input("Color: "))

                if zaxisstr != "":
                    zaxisstr += " & "
                zaxisstr += zaxis

                defvals = float(input("Default value?: "))
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
                        for name in net.inputs:
                            if name == xaxis:
                                net.setNode(name, x)
                            elif name == yaxis:
                                net.setNode(name, y)
                            else:
                                net.setNode(name, defvals)
                        net.process()
                        zvals.append(net.getNode(zaxis))
                        y += 0.1
                    x += 0.1

                #region ADD DATA
                userawpoints = False
                dataxvals = []
                datayvals = []
                datazvals = []
                datacolorvals = []

                if userawpoints:
                    if adddata == "y":
                        for item in data:
                            xval = gn.scale(datainputs[xaxis]["min"], item[xaxis], datainputs[xaxis]["max"], minx=-1, maxx=1)
                            yval = gn.scale(datainputs[yaxis]["min"], item[yaxis], datainputs[yaxis]["max"], minx=-1, maxx=1)

                            zval = gn.scale(dataoutputs[zaxis]["min"], item[zaxis], dataoutputs[zaxis]["max"], minx=-1, maxx=1)

                            dataxvals.append(xval)
                            datayvals.append(yval)
                            datazvals.append(zval)

                else:
                    datapoints = []
                    x = -1
                    while x <= 1:
                        y = -1
                        while y <= 1:
                            datapoints.append([x,y,0,0])
                            y += 0.1
                        x += 0.1

                    for item in data:
                        xval = gn.scale(datainputs[xaxis]["min"], item[xaxis], datainputs[xaxis]["max"], minx=-1,maxx=1)
                        yval = gn.scale(datainputs[yaxis]["min"], item[yaxis], datainputs[yaxis]["max"], minx=-1,maxx=1)
                        zval = gn.scale(dataoutputs[zaxis]["min"], item[zaxis], dataoutputs[zaxis]["max"], minx=-1,maxx=1)
                        for index in range(0, len(datapoints)):
                            if datapoints[index][0] -0.05 < xval < datapoints[index][0]+0.05 and datapoints[index][1] -0.05 < yval < datapoints[index][1]+0.05:
                                if zval > 0:
                                    datapoints[index][2] += zval
                                datapoints[index][3] += 1

                    for point in datapoints:
                        #print(point)
                        if point[3] > 0:
                            dataxvals.append(point[0])
                            datayvals.append(point[1])
                            datazvals.append(gn.scale(0, point[2]/point[3], 1))
                            datacolorvals.append(point[3])

                plt.scatter(xvals, yvals, zvals, color=color)
                gradientColors = True
                if adddata == "y":
                    if gradientColors:
                        #maxcolor = max(datacolorvals)
                        #for i in range(0, len(dataxvals)):
                        #color = gn.scale(0,datacolorvals[i],maxcolor,minx=0,maxx=1)
                        plt.scatter(dataxvals, datayvals, datazvals, s=datacolorvals, color="blue")
                    else:
                        plt.scatter(dataxvals, datayvals, datazvals, color="blue")
                #endregion ADD DATA

                if len(zaxisstr.split('&')) == len(net.outputs) or input("Done: ") == "y":
                    done = True
            plt.set_xlabel(xaxis)
            plt.set_ylabel(yaxis)
            plt.set_zlabel(zaxisstr)
            plt.set_title("Data from net: " + fname)
            pyplot.show()

        else:
            print("Mode not found")