import math
import random

class Node:
    # opposing force radius
    oppForceRadius = 100
    
    # should this node stay in place
    anchor = False
    
    x = 0
    y = 0
    
    def __init__(self, x, y, anchor=False, oppForceRadius=100):
        self.x = x
        self.y = y
        self.anchor = anchor
        self.oppForceRadius = oppForceRadius
    
    def checkForIntruders(self, nodeList):
        for node in nodeList:
            if (self.x == node.x and self.y == node.y):
                continue
            
            #if ((Math.abs(Math.abs(self.x) - Math.abs(node.x)) < 50) || (Math.abs(Math.abs(self.y) - Math.abs(node.y)) < 50))
            
            # if closer than oppForceRadius, cheap and imprecise math here
            if ((abs(self.x - node.x) < self.oppForceRadius) and (abs(self.y - node.y) < self.oppForceRadius)):
                self.pushAway(node)    
    
    def moveToward(self, otherNode):
        self.x += (otherNode.x - self.x) / 100
        self.y += (otherNode.y - self.y) / 100
    
    def pushAway(self, otherNode):
        otherNode.x += (otherNode.x - self.x) / 100
        otherNode.y += (otherNode.y - self.y) / 100

    def render(self):
        circle(self.x, self.y, 10)


class Edge:
    eLength = 200
    
    nodeOne = {}
    nodeTwo = {}
    
    def __init__(self, eLength, nodeOne, nodeTwo):
        self.eLength = eLength
        self.nodeOne = nodeOne
        self.nodeTwo = nodeTwo
    
    # run after checking for intruders on all Nodes
    def validateEnds(self):
        # if end Nodes are too far away, bring them back toward each other
        distance = math.sqrt((abs(self.nodeOne.x - self.nodeTwo.x) ** 2) + (abs(self.nodeOne.y - self.nodeTwo.y) ** 2))
        if (distance > self.eLength * 1.1):
            self.nodeTwo.moveToward(self.nodeOne)
        elif (distance < self.eLength * 0.9):
            self.nodeTwo.pushAway(self.nodeOne)
            
    def render(self):
        line(self.nodeOne.x, self.nodeOne.y, self.nodeTwo.x, self.nodeTwo.y)


def randomNode():
    return Node(random.randint(100, 700), random.randint(100, 700))

""" 
basic program flow:
    build nodes, then edges
    repeat however many times are necessary to feel confident:
        clear screen
        run checkForIntruders on all nodes
        run validateEnds on all edges
        render all nodes and edges
"""

WIDTH = 800
HEIGHT = 800

checksRemaining = 200

draw_c = color(100,100,100)

#nodeList = [Node(400, 450), Node(375, 425), Node(325, 460), Node(450, 415), Node(200, 450), Node(575, 325), Node(125, 460), Node(350, 615)]

nodeList = []
for i in range(8):
    nodeList.append(randomNode())

edgeList = [Edge(200, nodeList[0], nodeList[1]), Edge(200, nodeList[2], nodeList[3]), Edge(200, nodeList[1], nodeList[2]),
            Edge(200, nodeList[4], nodeList[5]), Edge(200, nodeList[6], nodeList[7]), Edge(200, nodeList[5], nodeList[2]),
            Edge(200, nodeList[0], nodeList[4])]

#nodeList = [Node(100, 100), Node(600, 600)]
#edgeList = [Edge(200, nodeList[0], nodeList[1])]


def setup():
    size(WIDTH, HEIGHT)
    background(255)
    frameRate(30)

def draw():
    global checksRemaining, nodeList, edgeList, draw_c
    background (255)
    for node in nodeList:
        node.render()
    for edge in edgeList:
        edge.render()
    if (checksRemaining > 0):
        # gross, O(n^2)
        for node in nodeList:
            node.checkForIntruders(nodeList)
        for edge in edgeList:
            edge.validateEnds()
        checksRemaining -= 1
