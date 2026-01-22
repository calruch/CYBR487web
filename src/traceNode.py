#! /bin/env python3

class TraceNode:
    '''  
    name: TraceNode
    description: Class to represent a node in a traceroute path.

    '''
    def __init__(self, nodeID, IPAddress, prevNode = None, nextNode = None):
        '''  
        name: TraceNode
        '''
        self.nodeID = nodeID
        self.IPAddress = IPAddress
        self.services = [] # Port or service - placeholder for future use

        # Linking nodes
        if prevNode is not None: self.prevNode = prevNode
        else: self.prevNode = None
        if nextNode is not None: self.nextNode = nextNode
        else: self.nextNode = None
    
    def getNodeID(self):
        '''  
        name: getNodeID
        description: Returns the node ID.
        '''
        return self.nodeID
    
    def getIPAddress(self):
        '''  
        name: getIPAddress
        description: Returns the IP address of the node.
        '''
        return self.IPAddress
    
    def getPrevNode(self):
        '''  
        name: getPrevNode
        description: Returns the previous node in the path.
        '''
        return self.prevNode
    def getNextNode(self):
        '''  
        name: getNextNode
        description: Returns the next node in the path.
        '''
        return self.nextNode
    def setPrevNode(self, prevNode):
        '''
        name: setPrevNode
        description: Sets the previous node in the path.
        '''
        self.prevNode = prevNode

    def setNextNode(self, nextNode):
        '''
        name: setNextNode
        description: Sets the next node in the path.
        '''
        self.nextNode = nextNode

class TracePath:
    '''  
    name: TracePath
    description: Class to represent a traceroute path consisting of multiple TraceNodes (linked list).

    '''
    def __init__(self):
        '''  
        name: TracePath
        '''
        self.source = None
        self.head = None
        self.tail = None
        self.length = 0
    
    def addNode(self, nodeID, IPAddress):
        '''  
        name: addNode
        description: Adds a new TraceNode to the path.
        '''
        newNode = TraceNode(nodeID, IPAddress)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.setNextNode(newNode)
            newNode.setPrevNode(self.tail)
            self.tail = newNode
    
    def getPath(self):
        '''  
        name: getPath
        description: Returns a list of IP addresses in the traceroute path.
        '''
        path = []
        currentNode = self.head
        while currentNode is not None:
            path.append(currentNode.getIPAddress())
            currentNode = currentNode.getNextNode()
        return path
    
    def rotatePath(self, ipAddress):
        '''  
        name: rotatePath
        description: Reverses the traceroute path to the specified IP.
        '''
        currentNode = self.head
        prevNode = None

        pass