import MachineLearning.GeneticNets as gn

def create(file, inputLen, outputLen, midWidth, midDepth, useNeat, useBias, activation_func, fin_activation_func):
    inputs = []
    for i in range(0, inputLen):
        inputs.append("Input" + str(i))
    outputs = []
    for i in range(0, outputLen):
        outputs.append("Output" + str(i))
    netDB = gn.Random(inputs, outputs, 1, midWidth, midDepth, bias=useBias, neat=useNeat,
              activation_func=activation_func,
              final_activation_func=fin_activation_func)

    gn.saveNets([netDB[0][0]], file, "EmptyNet", 1.0)