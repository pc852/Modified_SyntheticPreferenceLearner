# File: simple_cpynet.py
# Author: Michael Huelsman
# Created: 3 April 2020
# Purpose:
#   Builds classes which are useful for handling CP-nets whose domains have
#   attributes with only numerical values.
# Notes:
#   1) Assumes that the CP-net in question has complete CPTs.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import random
from .cpynet import CPYnet, generate_CPYNet
from utility.preference_graph import PreferenceGraph
from utility.conditional_preferences import ConditionalPreference
from examples.domain import Domain
from examples.alternative import Alternative

# A class whose objects represents a CP-net.
class CPnet:
    # Precond:
    #   None
    #
    # Postcond:
    #   Builds a blank CPnet with no nodes.
    def __init__(self):
        self.nodes = []
        self.domain = None

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the list of known variables in the CPNet.
    def prefVariables(self):
        return range(len(self.nodes))

    # Precond:
    #   alternative is a list of integers and a valid alternative in the domain.
    #
    # Postcond:
    #   Iterates through the list of neighbors to the
    #   alternative(hamming distance 1).
    def neighbors(self, alternative):
        result = Alternative(alternative.values,self.domain)
        for i in range(self.domain.length()):
            for j in range(self.domain.attr_length(i)):
                if j+1 == alternative.value(i):
                    continue
                result.set(i,j+1)
                yield result
            result.set(i,alternative.value(i))

    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds and returns the induced preference hypercube graph.
    def induced(self):
        result = PreferenceGraph(self.domain)
        for alternative in self.domain.each():
            for neighbor in self.neighbors(alternative):
                if self.compare_neighbors([alternative,neighbor]):
                    result.arc(alternative,neighbor)
        return result

    # Precond:
    #   alternatives is a list containing two neighboring alternatives.
    #
    # Postcond:
    #   Return true if the first alternative is preferred to the second alternative.
    def compare_neighbors(self, alternatives):
        diff = -1
        for i in range(self.domain.length()):
            if alternatives[0].value(i) != alternatives[1].value(i):
                diff = i
                break
        if diff == -1:
            return False
        vals = [alternatives[0].value(diff),alternatives[1].value(diff)]
        pref = None
        for cond in self.nodes[diff]:
            if cond.matches(alternatives[0]):
                pref = cond.get_order()
        if pref is None:
            return False
        vals = list(map(lambda x: pref.index(x),vals))
        return vals[0] < vals[1]

    # Precond:
    #   net is a valid CPnet object.
    #
    # Postcond:
    #   Converts a given CPnet object into a simple CP-net object.
    def convert(self,net):
        numbering = list(net.domain.keys())
        conversions = []
        # Convert the domain.
        # Keep record of everythings numberical conversions.
        attr_vals = []
        for attr in numbering:
            attr_vals.append(len(net.domain[attr]))
            conversions.append(net.domain[attr])
        self.domain = Domain(len(numbering),attr_vals)
        # Convert the nodes
        for attr in numbering:
            self.nodes.append([])
            for cond in net.nodes[attr]:
                temp = ConditionalPreference.convert_CPYNet(cond, numbering, conversions, attr)
                self.nodes[-1].append(temp)
                del temp
        return

    # Precond:
    #   filename is the name of the file to parse.
    #
    # Postcond:
    #   Modifies the CP-net to match the CP-net in the file.
    def load(self, filename):
        net = CPYnet()
        net.load(filename)
        self.convert(net)
        del net

    # Precond:
    #   None.
    #
    # Postcond:
    #   Converts the object into a string for printing.
    def __str__(self):
        result = ""
        for attr in self.nodes:
            for cond in attr:
                result += str(cond) + "\n"
            result += "\n"
        return result

    # Precond:
    #   info is a dictionary containing all needed generating information.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns a the preference graph of a random CP-net that has been closed
    #   under transitivity.
    @staticmethod
    def random(domain, info):
        net = generate_CPYNet(info, domain)
        simp_net = CPnet()
        simp_net.convert(net)
        ind = simp_net.induced()
        ind.transitive()
        return ind

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified LPM
    @staticmethod
    def pill_label(domain, info):
        des = ['CP-Net',str(info['indegree']),str(domain.length()),str(domain.attr_length_largest())]
        return ';'.join(des)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "CP-net"

    # Precond:
    #   filename is a string and a valid file name.
    #
    # Postcond:
    #   Writes a .dot file for the cp-net to the given filename.
    def write_dot(self, filename):
        with open(filename, 'w') as fout:
            fout.write("digraph {\n")
            for i in range(len(self.nodes)):
                fout.write(str(i)+";\n")
                conds = self.conditioners(i)
                for j in conds:
                    fout.write(str(j) + ' -> ' + str(i) + ";\n")
            fout.write('}')
