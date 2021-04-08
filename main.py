mode = str(input("Net/Genetic/Analyze/Interactive/Report/Template/Graph: "))

if mode == "Net":
    #Net demo
    import NetDemo
    NetDemo.run()

elif mode == "Genetic":
    #Game demo of the genetic alg
    import GeneticAlgDemo
    GeneticAlgDemo.run()

elif mode == "Analyze":
    import NetAnalyzer
    net = str(input("File name: "))
    NetAnalyzer.analyze(net)

elif mode == "Interactive":
    import InteractiveGrapher
    #net = str(input("File name: "))
    net = 'testnet'
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