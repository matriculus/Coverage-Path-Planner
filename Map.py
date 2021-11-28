import numpy as np
from utils import *

class Map:
    def __init__(self, map=[[0,0], [0,0]]):
        self.setMap(map)
        self.initialize()
    
    def setMap(self, map):
        self.map = np.array(map)
    
    def initialize(self):
        pos = np.where(self.map == 0)
        self.map[pos[0], pos[1]] = Status.FREE
        pos = np.where(self.map == 1)
        self.map[pos[0], pos[1]] = Status.OCCUPIED
        pos = np.where(self.map == 2)
        self.map[pos[0], pos[1]] = Status.START
        pos = np.where(self.map == 3)
        self.map[pos[0], pos[1]] = Status.END
        pos = np.where(self.map == 4)
        self.map[pos[0], pos[1]] = Status.VISITED

    def __str__(self):
        return str(self.map)
    
    def getSize(self):
        return np.array([self.map.shape[0], self.map.shape[1]])
    
    def getMinSize(self):
        return min(self.getSize())
    
    def getStatus(self, row, col):
        return self.map[row, col]
    
    def getStartPosition(self):
        loc = np.where(self.map == Status.START)
        return (loc[0][0], loc[1][0])
    
    def applyPath(self, path):
        for row, col in path:
           self.markVisited(row, col)
    
    def markVisited(self, row, col):
        if self.map[row, col] == Status.FREE:
            self.map[row, col] = Status.VISITED
    
    def allVisited(self):
        if self.map.all():
            return True
        
    def isOccupied(self, rows, cols):
        mapval = self.map[rows, cols]
        return (mapval == Status.OCCUPIED).all()

if __name__ == "__main__":
    from maps import *
    map = Map(map3)
    print(map)