class Node:

    def __init__(self, name, obj):

        self.name = name
        self.obj = obj



class Edge:

    def __init__(self, source, target):

        self.source = source
        self.target = target



class Graph:

    def __init__(self, nodes, edges):

        self.nodes = nodes
        self.edges = edges

        self.num_nodes = len(nodes)
        self.num_edges = len(edges)
        self.graph = self.build_graph()
    

    #builds the graph with regards to the target and source in the edges

    def build_graph(self):

        graph = {}

        for node in self.nodes:

            graph[node.name] = []

        for edge in self.edges:

            graph[edge.source.name].append(edge.target.name)

        return graph
