# File: clpm.py
# Author: Michael Huelsman
# Created On: 8 May 2020
# Purpose:
#   Holds a class for dealing with and generating CLPMs.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from random import randint, shuffle, sample
from utility.conditional_preferences import CPT
from examples.relation import Relation

# A class for holding CLPMs.
class CLPM:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns an empty CLPM.
    def __init__(self, domain):
        self.domain = domain
        self.attr_order = []
        self.preferences = []

    # Precond:
    #   alt1 is a valid Alternative object which is a member of the model's
    #       domain.
    #   alt2 is a valid Alternative object which is a member of the model's
    #       domain.
    #
    # Postcond:
    #   Returns the reslation between two alternatives as determined by the
    #   model.
    def compare(self, alt1, alt2):
        for rank in self.attr_order:
            rel = Relation.equal()
            for attr in rank:
                if(alt1.value(attr) != alt2.value(attr)):
                    attr_rel = self.preferences[attr].compare(alt1,alt2)
                    if rel == Relation.equal():
                        rel = attr_rel
                    elif not (rel == attr_rel):
                        return Relation.incomparable()
            if not (rel == Relation.equal()):
                return rel
        return Relation.equal()

    # Precond:
    #   info is a dictionary containing all needed generating information.
    #       limit: An integer indicating the maximum number of conditioning
    #           attributes.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns a the preference graph of a random CP-net that has been closed
    #   under transitivity.
    @staticmethod
    def random(domain, info):
        result = CLPM(domain)
        # Generate the (potentially grouped) attribute order.
        attrs = [i for i in range(domain.length())]
        shuffle(attrs)
        order = []
        while len(attrs) > 0:
            split = randint(1,len(attrs))
            order.append(attrs[0:split])
            attrs = attrs[split:]
        result.attr_order = order
        # Generate the preferences for each attribute
        prefs = [None for i in range(domain.length())]
        previous = []
        for group in order:
            for mem in group:
                limit = min(info['c_limit'],len(previous))
                num_conds = randint(0,limit)
                conds = sample(previous, num_conds)
                prefs[mem] = CPT.random(domain,conds,mem)
            previous.extend(group)
        result.preferences = prefs
        return result

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified LPM
    @staticmethod
    def pill_label(domain, info):
        des = ['CLPM',str(info['c_limit']),str(domain.length()),str(domain.attr_length_largest())]
        return ';'.join(des)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "CLPM"
