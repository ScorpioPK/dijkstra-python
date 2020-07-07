import numpy


class Graph:
    def __init__(self):
        self.node_number = 0
        self.edge_number = 0
        self.source_node = 0
        self.edges = []
        self.is_zero_based = True

    def read_from_file(self, file_name, is_zero_based):
        self.is_zero_based = is_zero_based
        f = open(file_name, "r")
        self.node_number, self.edge_number, self.source_node = [int(x) for x in f.readline().split()]
        if self.is_zero_based:
            self.edges = numpy.empty(self.node_number, dtype=object)
            for x in range(self.node_number):
                self.edges[x] = []
            for edge in range(0, self.edge_number):
                source, destination, weight = [int(x) for x in f.readline().split()]
                self.edges[source].append([destination, weight])
            f.close()
        else:
            self.source_node = self.source_node + 1
            self.edges = numpy.empty(self.node_number + 1, dtype=object)
            for x in range(self.node_number + 1):
                self.edges[x] = []
            for edge in range(0, self.edge_number):
                source, destination, weight = [int(x) for x in f.readline().split()]
                self.edges[source+1].append([destination+1, weight])
            f.close()

    def print(self):
        print ("{} {} {}".format(self.node_number, self.edge_number, self.source_node))
        for node in range(int(self.is_zero_based is False), self.node_number + int(self.is_zero_based is False)):
            for edge in self.edges[node]:
                print("{} {} {}".format(node, edge[0], edge[1]))
