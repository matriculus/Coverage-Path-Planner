import numpy as np
from utils import *
from matplotlib import pyplot as plt
import networkx as nx
from Map import Map

class Node:
    def __init__(self, node_id, coord, startIndex=None):
        self.node_id = node_id
        self.coord = np.asarray(coord)
        self.loc = self.coord.mean(axis=0)
        self.startIndex = startIndex
        self.parent = None
        self.children = []
    
    def addChild(self, child):
        assert isinstance(child, Node)
        child.parent = self
        self.children.append(child)
    
    def __str__(self):
        s = ""
        s += f"<Node: {self.node_id}>"
        return s
    
    def __repr__(self):
        return self.__str__()
        
    def isStartNode(self):
        return True if self.startIndex is not None else False
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

class Graph:
    def __init__(self, edges):
        self.Graph = nx.Graph()
        self.Graph.add_edges_from(edges)
        self.MST = self.getMST()
    
    def draw(self, filename="map"):
        plt.figure()
        nx.draw(self.Graph, with_labels=True)
        plt.savefig(f"Graph_{filename}.png", format="png")
        plt.figure()
        nx.draw(self.MST, with_labels=True)
        plt.savefig(f"Minimum_Spanning_Tree_{filename}.png", format="png")
    
    def getMST(self):
        # Obtaining minimum spanning tree from graph
        return nx.minimum_spanning_tree(self.Graph)
    
class Tree:
    R = np.array([[0, 1], [-1, 0]])
    def __init__(self, mst, map):
        assert isinstance(mst, nx.Graph)
        assert isinstance(map, Map)
        self.map = map
        self.graph = mst
        self.root = None
        self.getTree()
    
    def getEdges(self):
        return list(self.graph.edges())
    
    def getEdgeOf(self, node):
        return list(self.graph.edges(node))
    
    def getNodes(self):
        return list(self.graph.nodes())
    
    def getTree(self):
        self.root = self.getStartNode()
        self.addChild(self.root)
    
    def addChild(self, node):
        for _, child in self.getEdgeOf(node):
            if child == node.parent:
                continue
            node.addChild(child)
            self.addChild(child)
            
    def getStartNode(self):
        startNode = [node for node in self.getNodes() if node.isStartNode()]
        return startNode[0]
        
    def print_tree(self, node):
        prefix = f"{node.get_level()} "
        spacer = ' ' * node.get_level()*3 + "|____" if node.parent else ""
        statement = prefix + spacer + f"{node}"
        print(statement)    
        for child in node.children:
            self.print_tree(child)
    
    def printTree(self):
        self.print_tree(self.root)
    
    def traversing(self):
        route = [None]
        path = []
        self.routing(self.root, route)
        route.append(None)
        idx = np.asarray([route[1].startIndex])
        for i in range(len(route)-2):
            v, idx = self.nearestCoord([route[i], route[i+1], route[i+2]], idx)
            path.append(v)
        path = np.vstack(path)
        return path, route
    
    def routing(self, node, route):
        # Generated the list of nodes to be traversed at each step
        route.append(node)
        for child in node.children:
            self.routing(child, route)
            route.append(node)
    
    def setDirection(self, idx):
        # special case when the previous or next nodes are None and to identify directions for clockwise movements
        if idx == 0:
            direction = np.array([0, 1])
        elif idx == 1:
            direction = np.array([1, 0])
        elif idx == 3:
            direction = np.array([0, -1])
        else:
            direction = np.array([-1, 0])
        return direction
    
    def nearestCoord(self, nodes, idx):
        node1, node2, node3 = nodes
        if node1 is None:
            direction2 = 0.5*(node3.loc - node2.loc)
            direction1 = self.setDirection(idx)
        
        elif node3 is None:
            direction1 = 0.5*(node2.loc - node1.loc)
            direction2 = self.setDirection(idx)
        else:
            direction1 = 0.5*(node2.loc - node1.loc)
            direction2 = 0.5*(node3.loc - node2.loc)

        rot = (direction1[0]*direction2[1] - direction1[1]*direction2[0])
        d = np.linalg.norm(direction1 + direction2)

        indices = []
        direction = direction1
        if rot < 0: # clockwise movment
            while len(idx) > 0:
                current_coord = node2.coord[idx]
                indices.append(idx)
                idx = location(node2.coord, current_coord + direction)
                if len(idx) == 0:
                    direction = direction2
                    idx = location(node2.coord, current_coord + direction)
        
        elif rot > 0: # anti-clockwise movement
            direction = direction2
            while len(idx) > 0:
                current_coord = node2.coord[idx]
                indices.append(idx)
                idx = location(node2.coord, current_coord + direction)
        
        else: # rot == 0, straight
            if d > 1:
                while len(idx) > 0:
                    current_coord = node2.coord[idx]
                    indices.append(idx)
                    idx = location(node2.coord, current_coord + direction)
                    if len(idx) == 0:
                        direction = direction2
                        idx = location(node2.coord, current_coord + direction)
            else: # U-turn for dead ends
                temp_dir = [self.R.dot(direction1), direction2]
                j = False
                while len(idx) > 0:
                    current_coord = node2.coord[idx]
                    indices.append(idx)
                    idx = location(node2.coord, current_coord + direction)
                    if len(idx) == 0:
                        direction = temp_dir[j]
                        idx = location(node2.coord, current_coord + direction)
                        j = not j
                direction = direction2
        
        if node3 is not None:
            idx2 = location(node3.coord, current_coord + direction)
        else:
            idx2 = None
        
        return node2.coord[np.hstack(indices), :], idx2
