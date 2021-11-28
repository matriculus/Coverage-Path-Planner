from utils import *
import os, shutil
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from Map import Map

MINWINDOWSIZE = 480
MAXWINDOWSIZE = 640
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Recorder:
    def __init__(self):
        self.folder = "Snaps"
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        
        os.makedirs(self.folder)
        self.num = 0
    
    def save(self, screen):
        filename = f"snap_{self.num:0{5}}.png"
        fname = os.path.join(self.folder, filename)
        pygame.image.save(screen, fname)
        self.num += 1

class Robot:
    def __init__(self, row=0, col=0, size=20):
        self.setSize(size)
        self.path = []
        self.updatePosition(row, col)
    
    def setSize(self, size=20):
        self.size = size // 2
        self.radius = int(self.size * 0.8)
    
    def updatePosition(self, row, col):
        self.x, self.y =  self.size * (2*col + 1), self.size * (2*row + 1)
        self.path.append((self.x, self.y))
    
    def drawRobot(self, surface):
        pygame.draw.circle(surface, color=BLUE, center=(self.x, self.y), radius=self.radius)

class Grid:
    def __init__(self, map):
        assert isinstance(map, Map)
        self.updateMap(map)
        mapSize = self.getSize()
        self.gridSize = 20
        self.window = mapSize * self.gridSize
        if max(self.window) > MAXWINDOWSIZE:
            self.gridSize = MINWINDOWSIZE // max(mapSize)
            self.window = mapSize * self.gridSize
        elif min(self.window) < MINWINDOWSIZE:
            self.gridSize = MAXWINDOWSIZE // max(mapSize)
            self.window = mapSize * self.gridSize
    
    def updateMap(self, map):
        assert isinstance(map, Map)
        self.map = map

    def getSize(self):
        return self.map.getSize()[::-1]

    def getWindow(self):
        return self.window
    
    def getGridSize(self):
        return self.gridSize
    
    def drawSingleGrid(self, surface, position=[0,0], status=Status.FREE):
        x, y = position
        
        if status == Status.START:
            colour = GREEN
        elif status == Status.OCCUPIED:
            colour = BLACK
        elif status == Status.END:
            colour = RED
        elif status == Status.VISITED:
            colour = YELLOW
        else:
            colour = WHITE

        rect = pygame.Rect(x, y, self.gridSize, self.gridSize)
        pygame.draw.rect(surface, colour, rect, 0)
        pygame.draw.rect(surface, BLACK, rect, 1)
    
    def drawGrid(self, surface):
        i = 0
        for x in range(0, self.window[0], self.gridSize):
            j = 0
            for y in range(0, self.window[1], self.gridSize):
                self.drawSingleGrid(surface, (x, y), status=self.map.getStatus(j, i))
                j += 1
            i += 1

class AppWindow:
    def __init__(self, map, initial_position=[0,0]):
        assert isinstance(map, Map)
        self.grid = Grid(map)
        self.window = self.grid.getWindow()
        row, col = initial_position
        self.robot = Robot(row, col, self.grid.getGridSize())
        
        self.initialize()
        self.running = True

        # Position of start
        self.start_x = 0
        self.start_y = 0
    
    def initialize(self):
        # Window initialization
        pygame.init()
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode(self.window, flags)
        self.caption = pygame.display.set_caption("Coverage Path Planning")
        self.clock = pygame.time.Clock()
        self.screen.fill(GREY)

    def runningStatus(self):
        return self.running
    
    def exit(self):
        self.running = False
        pygame.quit()
    
    def update(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.display.update()
        self.clock.tick(10)
    
    def updateMap(self, map):
        assert isinstance(map, Map)
        self.grid.updateMap(map)
        if map.allVisited():
            self.running = False
    
    def updateRobot(self, row=0, col=0):
        self.robot.updatePosition(row, col)
    
    def drawGrid(self):
        self.grid.drawGrid(self.screen)

    def drawRobot(self):
        self.robot.drawRobot(self.screen)

if __name__ == "__main__":
    from maps import *
    from random import randint

    map_ = Map(map3)
    initial_position = map_.getStartPosition()
    app = AppWindow(map_, initial_position)
    
    while app.runningStatus():
        r, c = randint(0, map_.getSize()[0]-1), randint(0, map_.getSize()[1]-1)
        map_.markVisited(r, c)
        app.updateRobot(r,c)
        app.updateMap(map_)
        app.drawGrid()
        app.drawRobot()
        app.update()
    
    app.exit()