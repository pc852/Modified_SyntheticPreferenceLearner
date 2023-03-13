# File: induced.py
# Author: Michael Huelsman
# Created: 8 July 2019
# Purpose:
#   Builds classes which are useful for handling induced preference graphs.


class PreferenceGraph:
    # Precond:
    #   domain is a list of integers indicating the domain of outcomes.
    #
    # Postcond:
    #   Builds an empty preference graph.
    def __init__(self, domain):
        self.domain = domain
        self.nodes = {}
        for outcome in self.each_outcome():
            self.nodes[str(outcome)] = [[],False]

    # Precond:
    #   start is a list of integers and a valid outcome in the domain.
    #   to is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Adds the arc to the graph.
    def arc(self, start, to):
        self.nodes[str(start)][0].append(str(to))

    # Precond:
    #   None.
    #
    # Postcond:
    #   Alters the graph to its transitive closure version.
    def transitive(self):
        self.unmark()
        for node in list(self.nodes.keys()):
            self.transtive_node(node)

    # Precond:
    #   node is the key for a node.
    #
    # Postcond:
    #   Computes the transitive closure for the node in question.
    def transtive_node(self, node):
        if self.nodes[node][1]:
            return
        self.nodes[node][1] = True
        for arc in self.nodes[node][0]:
            self.transtive_node(arc)
            for arc2 in self.nodes[arc][0]:
                if not self.has_arc(node,arc2):
                    self.nodes[node][0].append(arc2)

    # Precond:
    #   start is a list of integers and a valid outcome in the domain.
    #   to is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Reutrns true if there is a path from the start outcome
    #   to the to outcome, in the transitive closure.
    def transtive_path(self, start, to):
        s = str(start)
        t = str(to)
        for arc in self.nodes[s][0]:
            if arc == t:
                return True
        return False

    # Precond:
    #   start is a list of integers and a valid outcome in the domain.
    #   to is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Reutrns true if there is a path from the start outcome
    #   to the to outcome.
    def path(self, start, to):
        self.unmark()
        if str(start) == str(to):
            return False
        return self.path_internal(str(start),str(to))

    # Precond:
    #   start is a string.
    #   to is a string.
    #
    # Postcond:
    #   Reutrns true if there is a path from the start outcome
    #   to the to outcome.
    def path_internal(self, start, to):
        if start not in self.nodes.keys() or to not in self.nodes.keys():
            return False
        if self.nodes[start][1]:
            return False
        self.nodes[start][1] = True
        if to in self.nodes[start][0]:
            return True
        for outcome in self.nodes[start][0]:
            if self.path(outcome,to):
                return True
        return False

    # Precond:
    #   None.
    #
    # Postcond:
    #   Unmarks all nodes in the graph.
    def unmark(self):
        for key in self.nodes.keys():
            self.nodes[key][1] = False

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all incomparable pairs.
    def incomparable(self):
        result = []
        for outcome in self.each_outcome():
            if self.maximal_outcome(outcome):
                break
            for comp in self.each_outcome(self.next_outcome(outcome)):
                if not self.path(outcome,comp) and not self.path(comp,outcome):
                    yield (outcome,comp)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all incomparable pairs.
    def transtive_incomparable(self):
        result = []
        for outcome in self.each_outcome():
            if self.maximal_outcome(outcome):
                break
            for comp in self.each_outcome(self.next_outcome(outcome)):
                if not self.transtive_path(outcome,comp) and not self.transtive_path(comp,outcome):
                    yield (outcome,comp)

    # Precond:
    #   outcome is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Iterates through all the outcomes in the domain.
    #   If outcome is provided start at the given outcome.
    def each_outcome(self, outcome=None):
        result = []
        if outcome is not None:
            result = outcome[:]
        else:
            result = [1 for i in range(len(self.domain))]
        while not self.maximal_outcome(result):
            yield result
            result = self.next_outcome(result)
        yield result

    # Precond:
    #   outcome is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Returns the next outcome(in numberical order, little endian).
    def next_outcome(self, outcome):
        result = outcome[:]
        hold = 1
        for i in range(len(result)):
            if hold == 0:
                break
            result[i] += hold
            hold = 0
            if result[i] > self.domain[i]:
                result[i] = 1
                hold = 1
        return result

    # Precond:
    #   outcome is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Returns true if the outcome is maximal (little endian, numerical).
    def maximal_outcome(self, outcome):
        for i in range(len(outcome)):
            if outcome[i] != self.domain[i]:
                return False
        return True

    # Precond:
    #   start is a string representing a node.
    #   to is a string representing a node.
    #
    # Postcond:
    #   Returns true if there is an arc from start to to.
    def has_arc(self, start, to):
        for node in self.nodes[start][0]:
            if node == to:
                return True
        return False

    def print_graph(self):
        for outcome in self.nodes.keys():
            for to in self.nodes[outcome][0]:
                print(outcome,"->",to)
