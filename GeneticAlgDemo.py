import MachineLearning.GeneticNets as gn
import MachineLearning.GeneticEvolution as ge
import NetRenderPro as nr

import pygame
import random

#CONFIG
obstacles = {'tall': [30,40,0],
             'long': [40,30,0],
             'flying': [30,70,30],
             'blank': [45,45,15]}
STARTING_POS = 800
OBSTACLE_COLOR = (255,0,0)

GAME_RIGHT_X = 0
GAME_LEFT_X = 800
GAME_TOP_Y = 300
GAME_BOTTOM_Y = 550

def getObstacleByType(typeStr):
    info = obstacles[typeStr]
    return info[0], info[1], info[2]

class Obstacle:
    global STARTING_POS
    global OBSTACLE_COLOR

    global GAME_RIGHT_X
    global GAME_LEFT_X
    global GAME_TOP_Y
    global GAME_BOTTOM_Y

    def __init__(self, typeStr):
        self.type = typeStr
        self.width, self.height, self.distancefromground = getObstacleByType(typeStr)
        self.pos = STARTING_POS

    def draw(self, screen):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (GAME_RIGHT_X+self.pos, GAME_BOTTOM_Y-self.distancefromground-self.height,
                                                  self.width, self.height))

class ObstacleDB:
    global GAME_RIGHT_X
    global GAME_LEFT_X
    global GAME_TOP_Y
    global GAME_BOTTOM_Y

    def __init__(self):
        self.obstaclelist = []
        self.counter = 0
        self.lastobstacletime = 400

        self.speed = 4

        self.validobstacles = None
        self.newobstacle = None


        self.remove = []

    def newObstacle(self):
        self.validobstacles = ['tall', 'long']
        if self.counter > 25:
            self.validobstacles.append('flying')

        self.newobstacle = self.validobstacles[random.randint(0,len(self.validobstacles)-1)]
        self.obstaclelist.append(Obstacle(self.newobstacle))

    def advanceGame(self):
        self.counter += 1
        self.lastobstacletime += 1

        self.speed += 0.001

        self.remove = []
        for obstacle in self.obstaclelist:
            obstacle.pos -= round(self.speed)
            if obstacle.pos <= GAME_RIGHT_X - obstacle.width:
                self.remove.append(obstacle)

        for obstacle in self.remove:
            self.obstaclelist.remove(obstacle)

        if random.randint(0, self.lastobstacletime) > 75:
            self.lastobstacletime = 0
            self.newObstacle()

    def drawGame(self, screen):
        pygame.draw.rect(screen, (0,255,0), (GAME_RIGHT_X, GAME_BOTTOM_Y, GAME_LEFT_X-GAME_RIGHT_X, 10))
        for obstacle in self.obstaclelist:
            obstacle.draw(screen)

    def getNextObstacle(self, xpos):
        if len(self.obstaclelist) > 0:
            for obstacle in self.obstaclelist:
                if obstacle.pos > xpos - 50:
                    return obstacle
            return Obstacle('blank')
        else:
            return Obstacle('blank')

def getPlayersFromNets(NetDB):
    Players = []
    count = 0
    for pair in NetDB:
        Players.append(Player(pair[0],count))
        count += 1
    return Players

class Player:
    global GAME_BOTTOM_Y
    def __init__(self, net, count):
        self.net = net
        self.score = count * 25
        self.ypos = GAME_BOTTOM_Y
        self.yvel = 0
        self.height = 40
        self.dead = False

        self.xpos = 25 + count*25
        #self.xpos = 25

        self.inputDB = {}
        self.outputDB = {}
        self.nextObstacle = None

        self.doDuck = False
        self.doJump = False

    def jump(self, do):
        if do:
            if self.ypos == GAME_BOTTOM_Y:
                self.yvel += 10

    def duck(self, do):
        if do and self.ypos == GAME_BOTTOM_Y:
            self.height = 20
        else:
            self.height = 40

    def process(self, gameInfo):
        self.nextObstacle = gameInfo.getNextObstacle(self.xpos)

        self.inputDB = {'dis': self.nextObstacle.pos-self.xpos,
                        'height': self.nextObstacle.height,
                        'width': self.nextObstacle.width,
                        'offGround': self.nextObstacle.distancefromground,
                        'speed': gameInfo.speed}

        if self.nextObstacle.pos-self.xpos < 300:
            self.net.reset()
            self.net.receiveInput(self.inputDB)
            self.net.process()
            self.outputDB = self.net.getOutput()

            #region PlayerPos
            self.doJump = self.outputDB["jump"] > 0
            self.doDuck = self.outputDB["duck"] > 0

            if self.doDuck and self.doJump:
                if self.outputDB["jump"] > self.outputDB["duck"]:
                    self.jump(True)
                    self.duck(False)
                else:
                    self.duck(True)
                    self.jump(False)

            else:
                self.duck(self.doDuck)
                self.jump(self.doJump)

            self.ypos -= self.yvel

            if self.ypos < GAME_BOTTOM_Y:
                self.yvel -= 0.5

            else:
                self.ypos = GAME_BOTTOM_Y

            #endregion PlayerPos

            #Check player collisions
            if abs(self.nextObstacle.pos + self.nextObstacle.width/2 - self.xpos) < self.nextObstacle.width:
                if self.height + (GAME_BOTTOM_Y-self.ypos) < self.nextObstacle.distancefromground:
                    #print("under")
                    self.score += 10 #passed under obstacle
                elif (GAME_BOTTOM_Y-self.ypos) > self.nextObstacle.height+self.nextObstacle.distancefromground:
                    #print("over")
                    self.score += 10 #jumped over obstacle
                else:
                    #print("Dead")
                    self.dead = True
            else:
                #print("No obstacle")
                self.score += 1 #no obstacle
        else:
            self.score += 1 #no obstacle close

        return self.dead

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.xpos,self.ypos-self.height,20,self.height))

class PlayerDB:
    def __init__(self, NetDB):
        self.Players = getPlayersFromNets(NetDB)
        self.NetDB = []

        self.player = None
        self.index = 0
        self.best = None
        self.maxscore = 0

    def processNNs(self, gameInfo, screen):
        alldead = True
        self.index = 0
        for self.player in self.Players:
            if not self.player.dead:
                alldead = self.player.process(gameInfo) and alldead
                self.player.draw(screen, (0,0,100+self.index*(100/len(self.Players))))
            self.index += 1
        return alldead

    def getNetDB(self):
        self.NetDB = []
        for self.player in self.Players:
            self.NetDB.append([self.player.net, self.player.score])
        return self.NetDB

    def getHighestPlayer(self):
        self.best = self.Players[0]
        self.maxscore = self.Players[0].score


        for self.player in self.Players:
            if self.player.score > self.maxscore and not self.player.dead:
                self.maxscore = self.player.score
                self.best = self.player
        return self.best

def initNets():
    NetDB = gn.Random({'dis': {'min': 0, 'max': 300},
                       'height': {'min': 15, 'max': 70},
                       'width': {'min': 30, 'max': 50},
                       'offGround': {'min': 0, 'max': 30},
                       'speed': {'min': 4, 'max': 8}},
                       ['jump', 'duck'], 15, 1, 5, activation_func='relu', final_activation_func='relu')
    return NetDB

def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Genetic Algorithim Demo")
    NetDB = initNets()

    speed = True
    done = False
    evoRate = 5 #3
    Generation = 0
    while not done:
        alldead = False
        playerDB = PlayerDB(NetDB)
        obstacleDB = ObstacleDB()
        Generation += 1
        frame = 0
        while not alldead:
            if frame%30 == 0 or speed:
                screen.fill((200,200,200))
            else:
                pygame.draw.rect(screen, (200,200,200), (0,0,300,700))
                pygame.draw.rect(screen, (200,200,200), (300, 400, 800, 300))

            obstacleDB.advanceGame()
            obstacleDB.drawGame(screen)
            alldead = playerDB.processNNs(obstacleDB, screen)
            pygame.draw.rect(screen, (0,0,0), (250,50,500,350), width=5)
            bestplayer = playerDB.getHighestPlayer()
            bestplayer.draw(screen, (255,255,255))

            if frame%30 == 0 or speed:
                nr.ShowValuedNet(bestplayer.net, screen, 300,100,700,250, labelWidth=100)

            nr.message_display(screen, "Speed: " + str(round(obstacleDB.speed)), (100,100))
            nr.message_display(screen, "Score: " + str(round(bestplayer.score)), (100,150))
            nr.message_display(screen, "Generation: " + str(round(Generation)), (100, 200))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    alldead = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        speed = not speed
            if speed:
                clock.tick(50)
            frame += 1
        screen.fill((200,200,200))
        pygame.display.update()

        NetDB = playerDB.getNetDB()
        NetDB = ge.evolve(NetDB, evoRate)
        #evoRate = 0.95 * evoRate

    pygame.quit()
    fname = str(input("Save net? "))
    if fname != "":
        gn.saveNets([NetDB[0][0]], fname, "GA Demo", 1.0)

