import pygame

def createScreen(x, y, caption, resize=False):
    if resize:
        display = pygame.display.set_mode((x,y), pygame.RESIZABLE)
    else:
        display = pygame.display.set_mode((x,y))

    pygame.display.set_caption(caption)
    return display

def checkClose(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
    else:
        return False

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, pos, color=(255,0,0), size=30):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(str(text), largeText, color)
    TextRect.center = pos
    screen.blit(TextSurf, TextRect)

class Button:
    def __init__(self, x, y, width, depth, color, clickedColor = None, text="", textcolor = None, textsize = 30, toggle=False):
        self.x = x
        self.y = y
        self.width = width
        self.depth = depth

        self.centerpos = ((self.x + self.width/2), (self.y + self.depth/2))

        self.color = color
        if clickedColor is None:
            self.clickedColor = self.color
        else:
            self.clickedColor = clickedColor

        self.toggle = toggle
        self.updated = False
        self.state = False #default to not-clicked

        self.text = text
        self.textcolor = textcolor
        self.textsize = textsize

        self.currentColor = None

    def reset(self):
        self.updated = False
        if not self.toggle: #toggle buttons don't reset state on click
            self.state = False

    def recieveClick(self, loc):
        if self.x < loc[0] < self.x + self.width and self.y < loc[1] < self.y + self.depth:
            self.updated = True
            if self.toggle:
                self.state = not self.state
            else:
                self.state = True

    def draw(self, screen):
        if self.state:
            self.currentColor = self.clickedColor
        else:
            self.currentColor = self.color
        pygame.draw.rect(screen, self.currentColor, (self.x,self.y,self.width, self.depth))

        if self.text != "":
            message_display(screen, self.text, self.centerpos, self.textcolor, self.textsize)


class ButtonManager:
    def __init__(self):
        self.ButtonList = []
        self.eventList = {}

    def addButton(self, button):
        self.ButtonList.append(button)

    def resetEvents(self):
        for self.button in self.ButtonList:
            self.button.reset()

    def getEvents(self):
        self.eventList = {}
        for self.button in self.ButtonList:
            self.eventList[self.button] = self.button.state
        return self.eventList

    def recieveEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            loc = pygame.mouse.get_pos()
            for self.button in self.ButtonList:
                self.button.recieveClick(loc)

    def draw(self, screen):
        for self.button in self.ButtonList:
            self.button.draw(screen)
