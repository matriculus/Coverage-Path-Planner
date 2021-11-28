from maps import *
from utils import *
from Graph import *
from visualise import AppWindow, Recorder
from Map import Map
from video import save_video

def main():
    recorder = Recorder()
    map_ = Map(map1)
    fname = "map1"

    rows, cols = map_.getSize()
    if rows % 2 == 0:
        pass
    initial_position = map_.getStartPosition()
    k = 0
    nodes = []
    for i in range(0, rows, 2):
        r = (i, i + 1) if (i+1) < rows else [i]
        for j in range(0, cols, 2):
            c = (j, j + 1) if (j+1) < cols else [j]
            w = [(ri,ci) for ri in r for ci in c]
            if not map_.isOccupied(r, c):
                if initial_position in w:
                    startIndex = w.index(initial_position)
                else:
                    startIndex = None
                # creating nodes
                n = Node(k, w, startIndex)
                nodes.append(n)
                k += 1
    # creating pairs of nodes
    edges = find_pairs(nodes)

    # generating graph for nearby nodes
    edges = form_graph(edges)
    
    G = Graph(edges)
    G.draw(fname)
    T = Tree(G.MST, map_)
    T.printTree()
    path, route = T.traversing()
    # (row, col) path of the grid map taken by the robot
    print(path)
    
    app = AppWindow(map_, initial_position)

    i = 0
    while app.runningStatus() and i < len(path):
        r, c = path[i]
        map_.markVisited(r, c)
        app.updateRobot(r,c)
        app.updateMap(map_)
        app.drawGrid()
        app.drawRobot()
        app.update()
        recorder.save(app.screen)
        i += 1
    
    app.exit()
    save_video(fname)
    

if __name__ == "__main__":
    main()