# File: neighbor_graph.py
# Author: Michael Huelsman
# Created On: 28 April 2020
# Purpose:
#   A graph class for determining a hill climbing fitness landscape.


class NeighborGraph:
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds an empty NeighborGraph object.
    def __init__(self):
        self.nodes = {}


    # Precond:
    #   label is a string used to identify a node.
    #   value is the evaluation value for the node.
    #
    # Postcond:
    #   Adds a node with the given label and value to the graph.
    def add_node(self, label, value):
        if label not in self.nodes:
            self.nodes[label] = self._empty_node()
        self.nodes[label][0] = value

    # Precond:
    #   v1 is a string used to identify a node.
    #   v2 is a string used to identify a node.
    #   undirected is a boolean indicating if the arc should be undirected.
    #
    # Postcond:
    #   Adds the given arc to the graph.
    def add_arc(self,v1,v2,undirected=True):
        if v1 not in self.nodes:
            self.nodes[v1] = self._empty_node()
        if v2 not in self.nodes:
            self.nodes[v2] = self._empty_node()
        if v2 not in self.nodes[v1][1]:
            self.nodes[v1][1].append(v2)
        if undirected and v1 not in self.nodes[v2][1]:
            self.nodes[v2][1].append(v1)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a list of all local minima.
    def local_minima(self):
        result = []
        val = 0
        minima = False
        for key in self.nodes:
            minima = True
            val = self.nodes[key][0]
            for neighbor in self.nodes[key][1]:
                if self.nodes[neighbor][0] < val:
                    minima = False
                    break
            if minima:
                result.append(key)
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a list of all local maxima.
    def local_maxima(self):
        result = []
        val = 0
        maxima = False
        for key in self.nodes:
            maxima = True
            val = self.nodes[key][0]
            for neighbor in self.nodes[key][1]:
                if self.nodes[neighbor][0] > val:
                    maxima = False
                    break
            if maxima:
                result.append(key)
        return result


    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the value of the global minima.
    def global_minima(self):
        minima = None
        for key in self.nodes:
            if minima is None or self.nodes[key][0] < minima:
                minima = self.nodes[key][0]
        return minima

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the value of the global maxima.
    def global_maxima(self):
        maxima = None
        for key in self.nodes:
            if maxima is None or self.nodes[key][0] > maxima:
                maxima = self.nodes[key][0]
        return maxima

    # Precond:
    #   None.
    #
    # Postcond:
    #   returns the average value for a node.
    def average(self):
        total = 0.0
        for key in self.nodes:
            total += self.nodes[key][0]
        return total/len(self.nodes)

    def __len__(self):
        return len(self.nodes)

    # Precond:
    #   id is a strgin node id.
    #
    # Postcond:
    #   Returns the value at the given node.
    def get(self, id):
        if id in self.nodes:
            return self.nodes[id][0]
        return 0



    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the value of a new empty node.
    #   0: Evaluation value.
    #   1: list of neighbors.
    def _empty_node(self):
        return [0, []]
