# File: lp_tree.py
# Author: Michael Huelsman
# Created On: 29 Jan 2019
# Purpose:
#   Specifies a class for handling LP-tree Models.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from examples.relation import Relation
from utility.conditional_preferences import CPT
from random import shuffle, sample, random, randint

# Class for handling an LPTNode.
class LPTNode:
    # Precond:
    #   leaf is a boolean that indicates if this node is a leaf.
    #
    # Postcond:
    #   Builds an empty LPTNode.
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.attr = None
        self.cpt = None
        self.split = False
        self.children = []

    # Precond:
    #  alt1 is a valid Alternative object.
    #  alt2 is a valid Alternative object.
    #
    # Postcond:
    #   Compares the two Altenratives and returns a Relation object.
    #   If the comparison cannot be completed returns None.
    def compare(self, alt1, alt2):
        # Base case
        if self.leaf:
            return Relation.equal()
        # See if comparison happens on this node.
        if alt1.value(self.attr) == alt2.value(self.attr):
            # No comparison. Proceed down the tree.
            if self.split:
                c_index = self.cpt.order(alt1)
                c_index = c_index.index(alt1.value(self.attr))
                return self.children[c_index].compare(alt1,alt2)
            else:
                return self.children[0].compare(alt1,alt2)
        else:
            # Handle differences
            order = self.cpt.order(alt1)
            if order.index(alt1.value(self.attr)) < order.index(alt2.value(self.attr)):
                return Relation.strict_preference()
            elif order.index(alt1.value(self.attr)) > order.index(alt2.value(self.attr)):
                return Relation.strict_dispreference()
            else:
                return Relation.equal()


# Class for handling an entire LP-tree.
class LPTree:
    # Precond:
    #   domain is a valid domain object.
    #
    # Postcond:
    #   Builds an empty LP-tree.
    def __init__(self, domain):
        self.domain = domain
        self.root = None

    # Precond:
    #  alt1 is a valid Alternative object.
    #  alt2 is a valid Alternative object.
    #
    # Postcond:
    #   Compares the two Altenratives and returns a Relation object.
    #   If the comparison cannot be completed returns None.
    def compare(self, alt1, alt2):
        if (not alt1.matches(self.domain)) or not (alt2.matches(self.domain)):
            return None
        return self.root.compare(alt1,alt2)

    # Precond:
    #  domain is a valid Domain object.
    #   info is a dictionary containing all needed generating information.
    #       cp: True or False depending on whether or not there is conditional
    #           preferences (string value).
    #       c_limit: The limit on the number of conditioning attributes for any
    #           one attribute (only applies if cp is True).
    #       ci: True or False depending on whether or not there is conditional
    #           importance (string value).
    #       s_limit: The limit on the number of splits along any one route to
    #           from the root to a leaf (only applies if ci is True).
    #
    # Postcond:
    #   Returns a randomly generated LPTree ovject of the specified type.
    @staticmethod
    def random(domain, info):
        result = LPTree(domain)
        attrs = [i for i in range(domain.length())]
        cp = (info['cp'] == 1)
        c_limit = 0
        if cp:
            c_limit = info['c_limit']
        ci = (info['ci'] == 1)
        s_limit = 0
        if ci:
            s_limit = info['s_limit']
        result.root = LPTree._random(domain, [], attrs, c_limit, s_limit)
        return result

    # Precond:
    #   domain is a valid Domain object.
    #   before is a list of the attribute which have already been used.
    #   current is the list of attributes yet to be used.
    #   c_limit is the limit on the number of attributes that can condition
    #       the current node.
    #   s_limit is the limit on the number of splits that can exist on this
    #       path.
    #   node is the current node to build.
    #
    # Postcond:
    #   Builds out a randomly generated LPTree from the given node.
    @staticmethod
    def _random(domain, before, current, c_limit, s_limit):
        node = LPTNode()
        # Base Case:
        if len(current) == 0:
            node.leaf = True
            return node
        # Determine the attribute to be placed in the node.
        shuffle(current)
        node.attr = current[0]
        # Determine if this node is conditioned.
        limit = min(c_limit,len(before))
        cond_count = randint(0,limit)
        if random() < 0.5:
            cond_count = 0
        node.cpt = CPT.random(domain, sample(before,cond_count), node.attr)
        # Determine and handle a potential split
        if s_limit > 0 and (random() < 0.5 or s_limit <= len(current)):
            node.split = True
            node.children = [None for i in range(domain.attr_length(node.attr))]
            for i in range(domain.attr_length(node.attr)):
                node.children[i] = LPTree._random(domain, before+[current[0]], current[1:], c_limit, s_limit-1)
        else:
            node.split = False
            node.children = [None]
            node.children[0] = LPTree._random(domain, before+[current[0]], current[1:], c_limit, s_limit)
        return node

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified LPM
    @staticmethod
    def pill_label(domain, info):
        des = ['LP-tree',str(info['cp']),str(info['c_limit']),str(info['ci']),str(info['s_limit']),str(domain.length()),str(domain.attr_length_largest())]
        return ';'.join(des)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "LPTree"
