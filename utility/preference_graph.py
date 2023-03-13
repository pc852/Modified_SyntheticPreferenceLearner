# File: preference_graph.py
# Author: Michael Huelsman
# Created: 8 July 2019
# Purpose:
#   Builds classes which are useful for handling induced preference graphs.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from examples.relation import Relation

class PreferenceGraph:
    # Precond:
    #   domain is a list of integers indicating the domain of outcomes.
    #
    # Postcond:
    #   Builds an empty preference graph.
    def __init__(self, domain):
        self.closed = False
        self.domain = domain
        self.nodes = {}
        for outcome in domain.each():
            self.nodes[str(outcome)] = [set([]),False,False]

    # Precond:
    #   start is a valid Alternative object.
    #   to is a valid Alternative object.
    #
    # Postcond:
    #   Adds the arc to the graph.
    def arc(self, start, to):
        self.nodes[str(start)][0].add(str(to))
        self.closed = False

    # Precond:
    #   None.
    #
    # Postcond:
    #   Alters the graph to its transitive closure version.
    def transitive(self):
        if self.closed:
            return
        for node in list(self.nodes.keys()):
            self.unmark()
            reachable = set()
            self.reachable_node(node,reachable)
            self.nodes[node][0] |= reachable
        self.closed = True

    # Precond:
    #   nodes is a list of valid Alternative objects.
    #
    # Postcond:
    #   Unions the outgoing arcs between n1 and n2.
    def share_arcs(self, nodes):
        arcs = set([])
        for node in nodes:
            arcs |= self.nodes[str(node)][0]
        for node in nodes:
            self.nodes[str(node)][0] = arcs

    # Precond:
    #   node is the key for a node.
    #   reachable is the Set of nodes which are already reachable by the node.
    #
    # Postcond:
    #   Computes the nodes reachable from the node in question.
    def reachable_node(self, node, reached):
        if self.nodes[node][1]:
            return
        self.nodes[node][1] = True
        for arc in self.nodes[node][0]:
            reached.add(arc)
            self.reachable_node(arc, reached)


    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the proportion of nodes which are part of a cylce.
    def cyclicity(self):
        count = 0
        for node in self.nodes.keys():
            self.unmark()
            if self.find_cycle(node,node):
                count += 1
        return count/(float(len(self.nodes)))

    # Precond:
    #   start is the node whose cyclicity we are determining.
    #   current is the current node under consideration.
    #
    # Postcond:
    #   Returns true if start is part of a cycle.
    def find_cycle(self, start, current):
        if self.nodes[current][1]:
            return False
        self.nodes[current][1] = True
        for arc in self.nodes[current][0]:
            if arc == start:
                return True
            else:
                if self.find_cycle(start,arc):
                    return True
        return False


    # Precond:
    #   start is a valid Alternative object.
    #   to is a valid Alternative object.
    #
    # Postcond:
    #   Reutrns true if there is a path from the start outcome
    #   to the to outcome, in the transitive closure.
    def transitive_path(self, start, to):
        s = str(start)
        t = str(to)
        if t in self.nodes[s][0]:
            return True
        return False

    # Precond:
    #   start is a valid Alternative object.
    #   to is a valid Alternative object.
    #
    # Postcond:
    #   Reutrns true if there is a path from the start outcome
    #   to the to outcome.
    # TODO: FIX
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
    #   Releases all nodes in the graph.
    def release(self):
        for key in self.nodes.keys():
            self.nodes[key][2] = False

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all incomparable pairs.
    def incomparable(self):
        result = []
        for outcome in self.domain.each():
            for comp in self.domain.each(self.domain.next_alternative(outcome)):
                if not self.path(outcome,comp) and not self.path(comp,outcome):
                    yield (outcome,comp)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all incomparable pairs.
    def transitive_incomparable(self):
        result = []
        for outcome in self.domain.each():
            for comp in self.domain.each(self.domain.next_alternative(outcome)):
                if not self.transitive_path(outcome,comp) and not self.transitive_path(comp,outcome):
                    yield (outcome,comp)

    # Precond:
    #   start is a string representing a node.
    #   to is a string representing a node.
    #
    # Postcond:
    #   Returns true if there is an arc from start to to.
    def has_arc(self, start, to):
        return to in self.nodes[start][0]

    # Precond:
    #   alt1 is a a valid Alternative object.
    #   alt2 is a a valid Alternative object.
    #
    # Postcond:
    #   Returns the relation between the two alternatives according to the graph..
    def compare(self, alt1, alt2):
        self.transitive()
        if self.transitive_path(alt1,alt2) and self.transitive_path(alt2,alt1):
            return Relation.equal()
        if self.transitive_path(alt1,alt2):
            return Relation.strict_preference()
        if self.transitive_path(alt2,alt1):
            return Relation.strict_dispreference()
        return Relation.incomparable()


    def print_graph(self):
        for outcome in self.nodes.keys():
            for to in self.nodes[outcome][0]:
                print(outcome,"->",to)
