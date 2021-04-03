import pygame

def GetDisStart(start, end, count):
    """Gets distance between points and starting point given number of points"""
    if count > 2:
        return int(round((end-start) / (count-1))), start #because one point is at the start

    elif count == 1:
        return 0, int(round((0.5 * (end-start)) + start)) #only one point, so distance doesn't matter, but start does

    elif count == 2:
        dis = (end-start) / 2
        return int(round(dis)), int(round(start + dis/2))

    else:
        print("ERROR (get dis start): Count = 0")
        return None

class ColorManager:
    """quick way to encapsulate getColorByValue"""
    def __init__(self, negativeColor, zeroColor, positiveColor):
        self.positiveColor = positiveColor
        self.zeroColor = zeroColor
        self.negativeColor = negativeColor

    def getColorByValue(self, val):
        """returns colors based on if val is positive, 0, or negative"""
        if val < 0:
            return self.negativeColor
        if val > 0:
            return self.positiveColor
        if val == 0:
            return self.zeroColor
        print("Error: (get color by value) val is not >,<, or = 0")
        return None

class nodecord:
    """Holds information about a node for the purpose of rendering it"""
    def __init__(self, node, x, y, color, animation):
        self.node = node
        self.x = x
        self.y = y
        self.color = color
        self.animation = animation

class nodecordlist(list):
    def __init__(self):
        super().__init__()
        self.nodecords = []

    def append(self, obj):
        self.nodecords.append(obj)

    def get(self, node):
        for i in self.nodecords:
            if i.node == node:
                return i
        print("Error (get node cord list): item not found")
        return None

class nodeline:
    """Holds informatino about a connection between 2 nodes"""
    def __init__(self, node1, node2, x1, y1, x2, y2, color, color2, width, animation):
        self.node1 = node1
        self.node2 = node2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color
        self.width = round(abs(width))
        self.color2 = color2
        self.width2 = round(abs(width)/3)
        self.animation = animation




#colors
black = (0,0,0)
yellow = (100,200,0)
grey = (50,50,50)
red = (255,0,0)
blue = (0,0,200)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, pos, color=(255,0,0)):
    largeText = pygame.font.Font('freesansbold.ttf', 15)
    TextSurf, TextRect = text_objects(str(text), largeText, color)
    TextRect.center = pos
    screen.blit(TextSurf, TextRect)

def ShowValuedNet(net, screen, startx, starty, endx, endy, nodeSize = 12, connectionWeight = 10,
                  posiColor = yellow, negColor = grey, zeroColor = None,
                  conColor = red, invConColor = blue, offColor = grey,
                  useLabels = True, labelWidth = 50, animated=None, key=True):
    """draws a net on a given screen that also shows node and connection values"""

    if zeroColor is None:
        zeroColor = negColor #we consider 0 to be negative be default

    color = ColorManager(negColor, zeroColor, posiColor)
    color2 = ColorManager(invConColor, invConColor, conColor)

    if useLabels:
        nodex = startx + labelWidth
        nodemaxx = endx - labelWidth
    else:
        nodex = startx

        nodemaxx = endx

    nodecords = nodecordlist()

    nodexdis = int(((nodemaxx - nodex) / max((len(net.midnodes) + 1),1))) #add one because input row
    currentxpos = nodex

    nodeydis, currentypos = GetDisStart(starty, endy, len(net.inputs))
    for nodeName in net.inputs:
        message_display(screen, nodeName, (currentxpos-labelWidth/2, currentypos))
        node = net.inputs[nodeName]
        nodecords.append(nodecord(node, currentxpos, currentypos, color.getColorByValue(node.val), 0))
        currentypos += nodeydis

    rowcount = 0
    for row in net.midnodes:
        rowcount += 2
        currentxpos += nodexdis
        nodeydis, currentypos = GetDisStart(starty, endy, len(row))
        for node in row:
            nodecords.append(nodecord(node, currentxpos, currentypos, color.getColorByValue(node.val), rowcount))
            currentypos += nodeydis

    currentxpos += nodexdis

    nodeydis, currentypos = GetDisStart(starty, endy, len(net.outputs))
    for nodeName in net.outputs:
        message_display(screen, nodeName, (currentxpos + labelWidth / 2, currentypos))
        node = net.outputs[nodeName]
        nodecords.append(nodecord(node, currentxpos, currentypos, color.getColorByValue(node.val), rowcount+2))
        currentypos += nodeydis

    nodeLines = [] #(x1, y1, x2, y2, width, color)

    for nodeName in net.inputs:
        node = net.inputs[nodeName]
        for connectionNode in node.connections:
            startnode = nodecords.get(node)
            endnode = nodecords.get(connectionNode)
            if abs((node.connections[connectionNode])) > 0.1:
                nodeLines.append(nodeline(node, connectionNode,
                                          startnode.x, startnode.y,
                                          endnode.x, endnode.y,
                                          color2.getColorByValue(node.connections[connectionNode]),
                                          color.getColorByValue(node.connections[connectionNode]*node.val),
                                          node.connections[connectionNode]*connectionWeight, 1))


    rowcount = 1
    for row in net.midnodes:
        rowcount += 2
        for node in row:
            for connectionNode in node.connections:
                startnode = nodecords.get(node)
                endnode = nodecords.get(connectionNode)
                nodeLines.append(nodeline(node, connectionNode,
                                          startnode.x, startnode.y,
                                          endnode.x, endnode.y,
                                          color2.getColorByValue(node.connections[connectionNode]),
                                          color.getColorByValue(node.connections[connectionNode] * node.val),
                                          node.connections[connectionNode]*connectionWeight, rowcount))

    #time to start drawing stuff on screen
    for line in nodeLines:
        pygame.draw.line(screen, line.color, (line.x1, line.y1), (line.x2, line.y2), line.width)

    for line in nodeLines:
        if animated is None or line.animation <= animated:
            pygame.draw.line(screen, line.color2, (line.x1, line.y1), (line.x2, line.y2), line.width2)

    for node in nodecords.nodecords:
        if node.node in net.bias.connections:
            pygame.draw.circle(screen, invConColor, (node.x, node.y), nodeSize+2)
        if animated is None or node.animation <= animated:
            pygame.draw.circle(screen, node.color, (node.x, node.y), nodeSize)
        else:
            pygame.draw.circle(screen, offColor, (node.x, node.y), nodeSize)

    if key:
        pygame.draw.rect(screen, posiColor, (startx+50, endy+50, 25,25))
        message_display(screen, ">0", (startx+62, endy+62))
        pygame.draw.rect(screen, negColor, (startx + 100, endy + 50, 25, 25))
        message_display(screen, "<0", (startx + 112, endy + 62))
        pygame.draw.rect(screen, conColor, (startx + 150, endy + 50, 25, 25))
        message_display(screen, "*1", (startx + 162, endy + 62), color=(0,0,0))
        pygame.draw.rect(screen, invConColor, (startx + 200, endy + 50, 25, 25))
        message_display(screen, "*-1", (startx + 212, endy + 62), color=(0,0,0))
        pygame.draw.circle(screen, invConColor, (startx+100,endy+102),10)
        pygame.draw.circle(screen, posiColor, (startx+100, endy+102), 8)
        message_display(screen, " = -1 (bias)", (startx+150,endy+102))


    return nodecords.nodecords