import math
import random

WIDTH = 800
HEIGHT = 800

class Node:
    # opposing force radius
    oppForceRadius = 100
    
    # should this node stay in place
    anchor = False
    
    x = 0
    y = 0
    
    def __init__(self, x, y, anchor=False, oppForceRadius=70):
        self.x = x
        self.y = y
        self.anchor = anchor
        self.oppForceRadius = oppForceRadius
    
    def checkForIntruders(self, nodeList):
        for node in nodeList:
            if (self == node):
                continue
            
            nodeDist = nodeDistance(self, node)
            nodeDist = max(nodeDist, 1)

            # if closer than oppForceRadius, cheap and imprecise math here
            if (nodeDist < self.oppForceRadius):
                if (nodeDistance(self, DUMMY_CENTER_NODE) > nodeDistance(node, DUMMY_CENTER_NODE)):
                    self.pushAway(node, ((self.oppForceRadius * 2) / nodeDist))
                else:
                    node.pushAway(self, ((self.oppForceRadius * 2) / nodeDist))
    
    def moveToward(self, otherNode, strength=1):
        self.x += ((otherNode.x - self.x) / 80) * strength
        self.y += ((otherNode.y - self.y) / 80) * strength
        
        # self.x = abs(self.x)
        # self.y = abs(self.y)
    
        if (self.x < 0):
            self.x += 200
        if (self.y < 0):
            self.y += 200
    
    def pushAway(self, otherNode, strength=1):
        otherNode.x -= ((self.x - otherNode.x) / 80) * strength
        otherNode.y -= ((self.y - otherNode.y) / 80) * strength
        
        # otherNode.x = abs(otherNode.x)
        # otherNode.y = abs(otherNode.y)
        if (otherNode.x < 0):
            otherNode.x += 400
        if (otherNode.y < 0):
            otherNode.y += 400

    def render(self):
        circle(self.x, self.y, 10)

DUMMY_CENTER_NODE = Node(400, 400)

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
        global WIDTH, HEIGHT
        # if end Nodes are too far away, bring them back toward each other
        distance = nodeDistance(self.nodeOne, self.nodeTwo)
        distance = max(distance, 10)
        
        # TODO: if nodeOne closer to center, push it away; else, push nodeTwo away 
        if (nodeDistance(self.nodeOne, DUMMY_CENTER_NODE) > nodeDistance(self.nodeTwo, DUMMY_CENTER_NODE)):
            if (distance > self.eLength * 1.3):
                self.nodeTwo.moveToward(self.nodeOne, 5)
            elif (distance < self.eLength * 0.8):
                self.nodeOne.pushAway(self.nodeTwo, (self.eLength * 2 / (distance * 10)))
        else:
            if (distance > self.eLength * 1.3):
                self.nodeOne.moveToward(self.nodeTwo, 5)
            elif (distance < self.eLength * 0.5):
                self.nodeTwo.pushAway(self.nodeOne, (self.eLength * 2 / (distance * 10)))
            
    def render(self):
        line(self.nodeOne.x, self.nodeOne.y, self.nodeTwo.x, self.nodeTwo.y)


def randomNode():
    #return Node(random.randint(100, 700), random.randint(100, 700))
    return Node(random.randint(350, 450), random.randint(350, 450))

def randomEdges(howMany, nodeList, eLength=200):
    edges = []
    for i in range(howMany):
        edges.append(Edge(eLength, nodeList[random.randint(0, len(nodeList) - 1)], nodeList[random.randint(0, len(nodeList) - 1)]))
    return edges

def nodeDistance(nodeOne, nodeTwo):
    return math.sqrt(((nodeOne.x - nodeTwo.x) ** 2) + ((nodeOne.y - nodeTwo.y) ** 2))

""" 
basic program flow:
    build nodes, then edges
    repeat however many times are necessary to feel confident:
        clear screen
        run checkForIntruders on all nodes
        run validateEnds on all edges
        render all nodes and edges
"""

runTime = 2000
fr = 0


draw_c = color(100,100,100)

#nodeList = [Node(400, 450), Node(375, 425), Node(325, 460), Node(450, 415), Node(200, 450), Node(575, 325), Node(125, 460), Node(350, 615)]

nodeList = []
for i in range(175):
    nodeList.append(randomNode())

edgeList = randomEdges(200, nodeList, 150)
#edgeList = []

# edgeList = [Edge(100, nodeList[0], nodeList[1]), Edge(100, nodeList[2], nodeList[3]), Edge(100, nodeList[1], nodeList[2]),
#             Edge(100, nodeList[4], nodeList[5]), Edge(100, nodeList[6], nodeList[7]), Edge(100, nodeList[5], nodeList[2]),
#             Edge(100, nodeList[0], nodeList[4]),
#             Edge(100, nodeList[8], nodeList[9]), Edge(100, nodeList[10], nodeList[11]), Edge(100, nodeList[9], nodeList[10]),
#             Edge(100, nodeList[12], nodeList[13]), Edge(100, nodeList[14], nodeList[15]), Edge(100, nodeList[13], nodeList[0]),
#             Edge(100, nodeList[6], nodeList[14])]

#nodeList = [Node(100, 100), Node(600, 600)]
#edgeList = [Edge(200, nodeList[0], nodeList[1])]

def setup():
    size(WIDTH, HEIGHT)
    background(255)
    frameRate(30)

def draw():
    global runTime, fr, nodeList, edgeList, draw_c
    background (255)
    for node in nodeList:
        node.render()
    #for edge in edgeList:
        # edge.render()
    if (fr < runTime):
        # gross, O(n^2)
        for node in nodeList:
            node.checkForIntruders(nodeList)
        for edge in edgeList:
            edge.validateEnds()
        fr += 1
        saveFrame("frames/bw-####.png")
