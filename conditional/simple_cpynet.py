# File: simple_cpynet.py
# Author: Michael Huelsman
# Created: 8 July 2019
# Purpose:
#   Builds classes which are useful for handling CP-nets whose domains have
#   attributes with only numerical values.
# Notes:
#   1) Assumes that the CP-net in question has complete CPTs.

import random
from .cpynet import CPnet
from .preference_graph import PreferenceGraph

# A class whose objects represent a CPT entry.
# Conditions are represented by an outcome where:
#   1) If a number is >0 then a satisfying outcome must have that value.
#   2) If a number is =0 then the attribute is not considered.
class SimpleCondPref:
    # Precond:
    #   pref is a list which contains:
    #       The condition as expressed via list
    #       A list of values ordered from most preferred to least preferred.
    #
    # Postcond:
    #   Builds a new CondPref object with the given conditional
    #   preference.
    def __init__(self, pref):
        self.pref = pref

    # Precond:
    #   outcome is a list representing the current outcome to match
    #   against the condition
    #
    # Postcond:
    #   Returns True if the condition matches the outcome.
    #   Returns False otherwise.
    def match(self, outcome):
        for i in range(len(self.pref[0])):
            if self.pref[0][i] == 0:
                continue
            if self.pref[0][i] != outcome[i]:
                return False
        return True

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the preference order associated with the conditional preference.
    def prefOrder(self):
        return self.pref[1]

    # Precond:
    #   conv is a valid CondPref object.
    #   num is an array of all attributes.
    #   convers is a list of lists containing canconicalized values.
    #   over is the attribute being converted.
    #
    # Postcond:
    #   Coverts the given conv into a SimpleCondPref object and stores it in
    #   this object.
    def convert(self, conv, num, convers, over):
        self.pref = []
        condition = [0 for i in range(len(num))]
        # Convert the condition.
        for attr in conv.pref[0].keys():
            converted = convers[num.index(attr)].index(conv.pref[0][attr])+1
            condition[num.index(attr)] = converted
        self.pref.append(condition)
        self.pref.append([])
        # Convert the preference list.
        for val in conv.pref[1]:
            self.pref[1].append(convers[num.index(over)].index(val)+1)
        return

    # Precond:
    #   None.
    #
    # Postcond:
    #   Converts the object into a string for printing.
    def __str__(self):
        return str(self.pref[0]) + "," + str(self.pref[1])

# A class whose objects represents a CP-net.
class SimpleCPnet:
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds a blank CPnet with no nodes.
    def __init__(self):
        self.nodes = []
        self.domain = []

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the list of known variables in the CPNet.
    def prefVariables(self):
        return range(len(self.nodes))

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random outcome that is consistent with the CPnet's domain.
    def randomOutcome(self):
        outcome = []
        for i in range(len(self.domain)):
            outcome.append(random.randint(1,self.domain[i]))
        return outcome

    # Precond:
    #   outcome is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Iterates through the list of neighbors to the
    #   outcome(hamming distance 1).
    def neighbors(self, outcome):
        result = outcome[:]
        for i in range(len(result)):
            for j in range(self.domain[i]):
                if j+1 == outcome[i]:
                    continue
                result[i] = j+1
                yield result
            result[i] = outcome[i]

    # Precond:
    #   outcome is a list of integers and a valid outcome in the domain.
    #
    # Postcond:
    #   Iterates through all the outcomes in the domain.
    #   If outcome is provided start at the given outcome.
    def each_outcome(self, outcome=None):
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
    #   None.
    #
    # Postcond:
    #   Builds and returns the induced preference hypercube graph.
    def induced(self):
        result = PreferenceGraph(self.domain)
        for outcome in self.each_outcome():
            for neighbor in self.neighbors(outcome):
                if self.compare_neighbors([outcome,neighbor]):
                    result.arc(outcome,neighbor)
        return result

    # Precond:
    #   outcomes is a list containing two neighboring outcomes.
    #
    # Postcond:
    #   Return true if the first outcome is preferred to the second outcome.
    def compare_neighbors(self, outcomes):
        diff = -1
        for i in range(len(outcomes[0])):
            if outcomes[0][i] != outcomes[1][i]:
                diff = i
                break
        if diff == -1:
            return False
        vals = [outcomes[0][diff],outcomes[1][diff]]
        pref = None
        for cond in self.nodes[diff]:
            if cond.match(outcomes[0]):
                pref = cond.prefOrder()
        if pref is None:
            return False
        vals = list(map(lambda x: pref.index(x),vals))
        return vals[0] < vals[1]

    # Precond:
    #   outcomes is a list containing two neighboring outcomes.
    #   attr is an integer represent the attribute to compare on.
    #
    # Postcond:
    #   Compares the outcomes according to the given attribute.
    #   Returns 1 if outcome[0] is preferred over outcome[1]
    #   Returns 0 if outcome[0] the same as outcome[1]
    #   Return -1 if outcome[1] is preferred over outcome[0]
    def attribute_compare(self, outcomes, attr):
        vals = [outcomes[0][attr],outcomes[1][attr]]
        pref = None
        for cond in self.nodes[attr]:
            if cond.match(outcomes[0]):
                pref = cond.prefOrder()
        if pref is None:
            return False
        vals = list(map(lambda x: pref.index(x),vals))
        if vals[0] < vals[1]:
            return 1
        elif vals[0] > vals[1]:
            return -1
        else:
            return 0

    # Precond:
    #   outcomes is a list containing two neighboring outcomes.
    #
    # Postcond:
    #   Compares the outcomes according to the aggregated lexicogrpahic
    #   evaluation.
    #   Returns 1 if outcome[0] is preferred over outcome[1]
    #   Returns 0 if outcome[0] is incomparable to outcome[1]
    #   Return -1 if outcome[1] is preferred over outcome[0]
    def lex_eval_compare(self, outcomes):
        equiv = []
        for i in range(len(outcomes[0])):
            if outcomes[0][i] == outcomes[1][i]:
                equiv.append(i)
        ignore = []
        removed = True
        while removed:
            removed = False
            for attr in range(len(outcomes[0])):
                if attr not in equiv or attr in ignore:
                    continue
                if not self.has_conditioners(attr, ignore):
                    ignore.append(attr)
                    removed = True

        comps = self.decisionRank(ignore)
        total = 0
        for comp in comps:
            total += self.attribute_compare(outcomes,comp)
        if abs(total) != len(comps):
            return 0
        if total < 0:
            return -1
        if total > 0:
            return 1
        return 0

    # Precond:
    #   ignore is a list of integers indicating which attributes to ignore.
    #
    # Postcond:
    #   Returns a list of the most important attributes still under
    #   consideration.
    def decisionRank(self, ignore):
        result = []
        for attr in range(len(self.nodes)):
            if attr in ignore:
                continue
            if not self.has_conditioners(attr, ignore):
                result.append(attr)
        return result

    # Precond:
    #   attr is the index of the attribute to consider.
    #   ignore is a list of integers indicating which attributes to ignore.
    #
    # Postcond:
    #   Returns the attributes which are conditioning the given attribute.
    def conditioners(self, attr, ignore=[]):
        result = []
        for i in range(len(self.nodes[attr][0].pref[0])):
            if i in ignore:
                continue
            if self.nodes[attr][0].pref[0][i] != 0:
                result.append(i)
        return result

    # Precond:
    #   attr is the index of the attribute to consider.
    #   ignore is a list of integers indicating which attributes to ignore.
    #
    # Postcond:
    #   Returns true if the attribute is still conditioned.
    def has_conditioners(self, attr, ignore=[]):
        for i in range(len(self.nodes[attr][0].pref[0])):
            if i not in ignore and self.nodes[attr][0].pref[0][i] != 0:
                return True
        return False



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
        for attr in numbering:
            self.domain.append(len(net.domain[attr]))
            conversions.append(net.domain[attr])
        # Convert the nodes
        for attr in numbering:
            self.nodes.append([])
            for cond in net.nodes[attr]:
                temp = SimpleCondPref([])
                temp.convert(cond, numbering, conversions, attr)
                self.nodes[-1].append(temp)
                del temp
        return

    # Precond:
    #   filename is the name of the file to parse.
    #
    # Postcond:
    #   Modifies the CP-net to match the CP-net in the file.
    def load(self, filename):
        net = CPnet()
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
