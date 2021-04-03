import NetRenderPro
import MachineLearning.GeneticNets as gn
import pygame
from time import sleep
import copy

#colors
black = (0,0,0)
yellow = (100,200,0)
grey = (50,50,50)

squares = [1,1,1,1,0]

#config
nodeSize = 15

lastnodetest = [None, [[0,0,0,0]]]

def squareColor(pos, customList = None):
    global squares
    global yellow
    global grey
    global black
    if customList is None:
        customList = squares
    if customList[pos] == 1:
        return yellow
    elif customList[pos] == -1:
        return grey
    else:
        return black

def getNode(nodecords, loc, size):
    node = None
    x = loc[0]
    y = loc[1]
    for i in nodecords:
        if x-size < i.x < x+size and y-size < i.y < y+size:
            if node is not None:
                print("Error (get node): 2 nodes")
            node = i.node
    return node

def checkPos(pos):
    x = pos[0]
    y = pos[1]

    if 75 < x < 75+90 and 75 < y < 75 + 90:
        return 0
    elif 175 < x < 175+90 and 75 < y < 75 + 90:
        return 1
    elif 75 < x < 75+90 and 175 < y < 175 + 90:
        return 2
    elif 175 < x < 175+90 and 175 < y < 175 + 90:
        return 3
    return None

def runNet(net):
    global squares
    net.reset()
    net.setNode("A", squares[0])
    net.setNode("B", squares[1])
    net.setNode("C", squares[2])
    net.setNode("D", squares[3])
    net.process()
    if net.getNode("Out") > 0:
        squares[4] = 1
    else:
        squares[4] = -1

def possibilities(prevlist, values):
    out = []
    for minilist in prevlist:
        for val in values:
            newlist = copy.deepcopy(minilist)
            newlist.append(val)
            out.append(newlist)
    return out

def everyList(count, values):
    out = [[]]
    for i in range(0,count):
        out = copy.deepcopy(possibilities(out, values))
    return out

def testForNode(net, node):
    global lastnodetest
    if lastnodetest[0] == node:
        return lastnodetest[1]
    lists = everyList(4, [-1,1])
    istrue = []
    for inputset in lists:
        net.reset()
        net.setNode("A", inputset[0])
        net.setNode("B", inputset[1])
        net.setNode("C", inputset[2])
        net.setNode("D", inputset[3])
        net.process()

        output = node.val
        if output > 0:
            istrue.append(inputset)

    runNet(net) #to reset results
    if len(istrue) > 2:
        baselist = [None,None,None,None]
        for true in istrue:
            for index in range(0,4):
                if baselist[index] is None:
                    baselist[index] = true[index]
                elif baselist[index] != 0:
                    if baselist[index] != true[index]:
                        baselist[index] = 0
        out = [baselist]
    else:
        out = istrue
    lastnodetest[1] = out
    return out

def displayNodeInfo(screen, net, node, pos):
    x = pos[0]
    y = pos[1]

    ntype = type(node)
    if ntype == gn.inNode:
        ntype = "Input Node"
    elif ntype == gn.midNode:
        ntype = "Hidden Node"
    elif ntype == gn.outNode:
        ntype = "Output Node"


    act = "Activation: " + node.acivation_func
    val = "Outputting Value: " + str(round(node.val,3))
    inval = "Input Value Total: " + str(round(node.total,3))
    NetRenderPro.message_display(screen, ntype, (x+190, y+20))
    NetRenderPro.message_display(screen, act, (x+190, y+40))
    NetRenderPro.message_display(screen, inval, (x+190, y+60))
    NetRenderPro.message_display(screen, val, (x+190, y+80))

    x = 70
    lists = testForNode(net, node)
    dif = 60

    for baselist in lists:
        pygame.draw.rect(screen, black, (x, 500, 55, 55))
        pygame.draw.rect(screen, squareColor(0, customList = baselist), (x + 5, 505, 20, 20))
        pygame.draw.rect(screen, squareColor(1, customList = baselist), (x + 30, 505, 20, 20))
        pygame.draw.rect(screen, squareColor(2, customList = baselist), (x + 5, 530, 20, 20))
        pygame.draw.rect(screen, squareColor(3, customList = baselist), (x + 30, 530, 20, 20))
        x += dif

def run():
    print("Running net demo")
    net = gn.loadNets("diagonal-net")[0][0]
    runNet(net)

    pygame.init()

    screen = pygame.display.set_mode((800,625))
    pygame.display.set_caption("Net Demo")

    done = False
    animationStage = 6
    doanimation = "MANUAL"
    while not done:
        screen.fill((200,200,200))

        pygame.draw.rect(screen, black, (350,50,400,400), width = 5)
        pygame.draw.rect(screen, black, (50,50, 240,400), width = 5)
        pygame.draw.rect(screen, black, (50, 475, 700, 125), width=5)

        nodecords = NetRenderPro.ShowValuedNet(net, screen, 350,100,750,300, useLabels=True, labelWidth=75,
                                   nodeSize = nodeSize, connectionWeight=10, animated=round(animationStage))

        node = getNode(nodecords, pygame.mouse.get_pos(), nodeSize)
        if node is not None:
            displayNodeInfo(screen, net, node, (350, 475))

        pygame.draw.rect(screen, black, (60,60,220,220))
        pygame.draw.rect(screen, squareColor(0), (75,75,90,90))
        pygame.draw.rect(screen, squareColor(1), (175,75,90,90))
        pygame.draw.rect(screen, squareColor(2), (75, 175, 90, 90))
        pygame.draw.rect(screen, squareColor(3), (175, 175, 90, 90))

        NetRenderPro.message_display(screen, "A", (120,120))
        NetRenderPro.message_display(screen, "B", (220,120))
        NetRenderPro.message_display(screen, "C", (120,220))
        NetRenderPro.message_display(screen, "D", (220,220))


        pygame.draw.rect(screen, black, (100,290,130,130))
        pygame.draw.rect(screen, squareColor(4), (110,300,110,110))
        NetRenderPro.message_display(screen, "Frame: " + str(round(animationStage)), (700, 80))
        NetRenderPro.message_display(screen, "Mode: " + doanimation, (675,100))
        pygame.display.update()

        if doanimation == "AUTO":
            animationStage += 0.02
        if animationStage > 6:
            animationStage = 0
        if animationStage < 0:
            animationStage = 6
        elif doanimation == "OFF":
            animationStage = 6

        for event in pygame.event.get():
            loc = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                square = checkPos(loc)
                if square is not None:
                    squares[square] = squares[square] * -1
                    runNet(net)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if doanimation == "MANUAL":
                        doanimation = "OFF"
                    elif doanimation == "OFF":
                        doanimation = "AUTO"
                    elif doanimation == "AUTO":
                        doanimation = "MANUAL"
                        animationStage = 6
                if event.key == pygame.K_RIGHT:
                    animationStage += 1
                if event.key == pygame.K_LEFT:
                    animationStage -= 1
            if event.type == pygame.QUIT:
                done = True


        sleep(0.01)


    pygame.quit()
