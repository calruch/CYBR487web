#! /bin/env python3

import pydot

LETTERLIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']

class Visualizer:
    '''
    name: TraceVisualizer
    description: Class to visualize the traceroute path using pydot.
    '''
    def __init__(self, TreeHead):
        '''
        name: TraceVisualizer
        description: Initializes the Visualizer with a TraceTree.
        parameters: traceTree (TraceTree)
        '''
        self.head = TreeHead

    def generateGraph(self, outputFile='traceroute_graph.png'):
        '''
        name: generateGraph
        description: Generates a graphical representation of the traceroute path and saves it to a file.
        parameters: outputFile (string)
        '''
        graph = pydot.Dot("Network_Topology", graph_type='graph')

        # Add head node
        graph.add_node(pydot.Node(LETTERLIST[self.head.getID()], label=f"{self.head.getIPAddress()}\nHop: {self.head.getHop()}"))
        # Recursively add edges
        self.addEdges(self.head, graph)

        graph.write_png(outputFile)
 

    def addEdges(self, parent, graph):
        '''
        name: addEdges
        description: Recursively adds edges to the graph from the TraceTree.
        parameters: node (Node)
        '''
        for child in parent.getChildren():
            graph.add_node(pydot.Node(LETTERLIST[child.getID()], label=f"{child.getIPAddress()}\nHop: {child.getHop()}"))
            graph.add_edge(pydot.Edge(LETTERLIST[parent.getID()], LETTERLIST[child.getID()]))
            self.addEdges(child, graph)