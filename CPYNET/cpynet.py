# File: cpnet.py
# Author: Michael Huelsman
# Created: 5 July 2018
# Purpose:
#   Builds a class which represents a CP-network preference representation.

import xml.etree.ElementTree as xmlTree
import random

# A class whose objects represent a CPT entry.
class CondPref:
    # Precond:
    #   pref is a list which contains:
    #       The condition as expressed via a dictionary
    #       A list of values ordered from most preferred to least preferred.
    #
    # Postcond:
    #   Builds a new CondPref object with the given conditional
    #   preference.
    def __init__(self, pref):
        self.pref = pref

    # Precond:
    #   outcome is a dictionary representing the current outcome to match
    #       against the condition
    #
    # Postcond:
    #   Returns True if the condition matches the outcome.
    #   Returns False otherwise.
    def match(self, outcome):
        for key in self.pref[0].keys():
            if outcome[key] != self.pref[0][key]:
                return False
        return True

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the preference order associated with the conditional preference.
    def prefOrder(self):
        return self.pref[1]

# A class whose objects represents a CP-net.
class CPnet:
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds a blank CPnet with no nodes.
    def __init__(self):
        self.nodes = {}
        self.domain = {}

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the list of known variables in the CPNet.
    def prefVariables(self):
        return self.domain.keys()

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random outcome that is consistent with the CPnet's domain.
    def randomOutcome(self):
        outcome = {}
        for var in self.domain.keys():
            outcome[var] = random.choice(self.domain[var])
        return outcome

    # Precond:
    #   outcome is a dictionary representing a possible outcome as a starting
    #       point.
    #
    # Postcond:
    #   Returns a list of ordered outcomes based on the order induced by the
    #   CPnet.
    def outcomeList(self, outcome):
        result = [outcome.copy()]
        order = self.domain.keys()
        random.shuffle(order)
        # Decreasing sequence
        for key in order:
            if key in self.nodes:
                prefOrder = self.prefOrder(outcome, key)
                index = prefOrder.index(outcome[key])
                if index < len(prefOrder)-1:
                    index = random.randint(index+1, len(prefOrder)-1)
                    outcome[key] = prefOrder[index]
                    result.append(outcome.copy())
        # Increasing sequence
        outcome = result[0].copy()
        for key in order:
            if key in self.nodes:
                prefOrder = self.prefOrder(outcome, key)
                index = prefOrder.index(outcome[key])
                if index > 0:
                    index = random.randint(0, index-1)
                    outcome[key] = prefOrder[index]
                    result.insert(0,outcome.copy())
        return result


    # Precond:
    #   outcome is a dictionary representing an alternative.
    #   variable is a string denoting the varible whose preference order to
    #       retrieve.
    # Postcond:
    #   Returns the preference order for values of the specfied variable given
    #   the provided outcome. Returns None if variable is not a part of the
    #   CPnet or not preference order exists.
    def prefOrder(self, outcome, variable):
        if variable not in self.nodes:
            return None
        result = None
        for condition in self.nodes[variable]:
            if condition.match(outcome):
                result = condition.prefOrder()
                break
        return result



    # Precond:
    #   filename is the name of the file to parse.
    #
    # Postcond:
    #   Modifies the CP-net to match the CP-net in the file.
    def load(self, filename):
        self.nodes = {}
        net = xmlTree.parse(filename)
        net = net.getroot()
        for child in net:
            if child.tag == 'PREFERENCE-VARIABLE':
                name = ''
                for field in child:
                    if field.tag == 'VARIABLE-NAME':
                        name = field.text
                    if field.tag == 'DOMAIN-VALUE':
                        if name not in self.nodes:
                            self.nodes[name] = []
                        if name not in self.domain:
                            self.domain[name] = []
                        self.domain[name].append(int(field.text))
            elif child.tag == 'PREFERENCE-STATEMENT':
                condition = {}
                order = []
                variable = ''
                for field in child:
                    if field.tag == 'PREFERENCE-VARIABLE':
                        variable = field.text
                    if field.tag == 'CONDITION':
                        parts = field.text.split('=')
                        condition[parts[0]] = int(parts[1])
                    if field.tag == 'PREFERENCE':
                        parts = field.text.split(':')
                        order.append(list(map(lambda x: int(x), parts)))
                order = CPnet.sortOrder(order,self.domain[variable])
                if variable in self.nodes:
                    self.nodes[variable].append(CondPref([condition,order]))
                else:
                    self.nodes[variable] = []
                    self.nodes[variable].append(CondPref([condition,order]))

    # Precond:
    #   prefs is a sequence of preference pairs between two values with the
    #       first value being preferred to the second.
    #   values is a list of all the possible values to consider.
    #
    # Postcond:
    #   Returns an ordered list of values.
    @classmethod
    def sortOrder(cls, prefs, values):
        result = []
        vals = values[:]
        while len(result) != len(values):
            undom = vals[:]
            # Determine top option.
            for pref in prefs:
                if pref[1] in undom:
                    undom.remove(pref[1])
            # Add top values to the order.
            # Remove top values from consideration.
            for val in undom:
                result.append(val)
                vals.remove(val)
            # Remove used preference statements
            newPrefs = []
            for i in range(len(prefs)):
                if prefs[i][0] not in undom:
                    newPrefs.append(prefs[i])
            prefs = newPrefs[:]
            del newPrefs
        return result
