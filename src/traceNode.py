#! /bin/env python3

class Node:
    '''  
    name: TraceNode
    description: Class to represent a node in a traceroute path.

    '''

    def __init__(self, IPAddress, hop, ID , parent=None):
        '''  
        name: TraceNode
        description: Initializes the TraceNode with node ID and IP address.
        parameters: nodeID (int), IPAddress (string), prevNode (TraceNode), nextNode (TraceNode)
        '''
        self.IPAddress = IPAddress
        self.hop = hop
        self.ID = ID
        self.services = []  # Port or service - placeholder for future use
        self.children = []  # Placeholder for future use
        self.childrenCount = 0  # Placeholder for future use
        self.parent = parent


    def getIPAddress(self):
        '''  
        name: getIPAddress
        description: Returns the IP address of the node.
        '''
        return self.IPAddress

    def getHop(self):
        '''  
        name: getHop
        description: Returns the hop number of the node.
        '''
        return self.hop
    
    def getChildren(self):
        '''  
        name: getChildren
        description: Returns the children of the node.
        '''
        return self.children
    
    def addChild(self, childNode):
        '''  
        name: addChild
        description: Adds a child Node to this node.
        parameters: childNode (Node)
        '''
        self.children.append(childNode)
        self.childrenCount += 1
        childNode.setParent(self)

    def setParent(self, parentNode):
        '''  
        name: setParent
        description: Sets the parent Node of this node.
        parameters: parentNode (Node)
        '''
        self.parent = parentNode

    def getChildrenCount(self):
        '''  
        name: getChildrenCount
        description: Returns the number of children of this node.
        '''
        return self.childrenCount
    
    def getID(self):
        '''  
        name: getID
        description: Returns the ID of this node.
        '''
        return self.ID

class TraceTree:
    '''  
    name: TraceTree
    description: Class to represent a traceroute path consisting of multiple Nodes (linked list).

    '''

    def __init__(self, startIP):
        '''  
        name: TraceTree
        '''
        self.startIP = startIP
        self.head = Node(startIP, 0, ID=0)
        self.nodeCount = 1

    def addNode(self, IPAddress, hop, parentNode):
        '''  
        name: addNode
        description: Adds a new Node to the TraceTree.
        parameters: IPAddress (string), hop (int)
        '''
        newNode = Node(IPAddress, hop, ID=self.nodeCount, parent=parentNode)
        parentNode.addChild(newNode)
        self.nodeCount += 1
        return newNode

    def convertHopNode(self, hopList):
        '''  
        name: convertHopNode
        description: Converts a list of [hop, IPAddress, timeTaken] into a TraceNode.
        parameters: hopList (list)
        '''
        hop = hopList[0]
        IPAddress = hopList[1]
        newNode = Node(IPAddress, hop, ID=self.nodeCount)
        return newNode
    
        
    def findChildNode(self, parentNode, hop, current=None):
        '''  
        name : findChildNode
        description: Finds a child node of the given parent node that matches the specified hop.
        parameters: parentNode (Node), hop (list), current (Node)
        returns: Node or None
        '''
        for child in parentNode.getChildren():
            if child.getHop() == hop[0] and child.getIPAddress() == hop[1]:
                return child
        return None
    
    def convertListTree(self, traceList):
        '''  
        name: convertListTree
        description: Converts a list of[ [ [hop, IPAddress, timeTaken] ] ]into a TraceTree linked list.
        parameters: traceList (list)
        '''

        for trace in traceList: # each item is a traceroute result
            if trace is None:
                continue

            current = self.head

            for hop in trace: # each item is a hop [hop number, IP address, time taken]
                hopNum = hop[0]
                IPAddress = hop[1]
                

                existingNode = self.findChildNode(current, hop)
                if existingNode is not None:
                    current = existingNode
                else:
                    current = self.addNode(IPAddress, hopNum, current)
        
        return self.getTree()
    
    def getTree(self):
        '''
        name: getTree
        description: Returns the head node of the TraceTree.
        '''
        return self.head
    
    def printTree(self, node=None):
        '''
        name: printTree
        description: Prints the TraceTree starting from the given node.
        parameters: node (TraceNode)
        returns: none
        '''
        if node is None:
            node = self.head
        for child in node.getChildren():
            self.printTree(child)


