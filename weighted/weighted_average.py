# File: weighted_average.py
# Author: Michael Huelsman
# Created On: 13 Dec 2019
# Purpose:
#   Defines a class which handles weight average preference representations.

import sys, os
sys.path.insert(0, os.path.abspath('..'))


from random import random, shuffle
import math
from examples.relation import Relation

class WeightedAverage:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Builds a new empty WeightedAverage object.
    def __init__(self, domain):
        self.domain = domain
        self.orders = []
        self.weights = []

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the evaluation of the alternative.
    #   Returns 0 by default.
    def eval(self, alt):
        if not alt.matches(self.domain):
            return 0
        total = 0
        for i in range(len(self.weights)):
            total += self.orders[i].index(alt.value(i)-1)*self.weights[i]
        return total

    # Precond:
    #   alt1 is a valid Alternative object.
    #   alt2 is a valid Alternative object.
    #
    # Postcond:
    #   Returns the comparison of the alternatives.
    def compare(self, alt1, alt2):
        val1 = self.eval(alt1)
        val2 = self.eval(alt2)
        if val1 > val1:
            return Relation.strict_preference()
        elif val1 < val2:
            return Relation.strict_dispreference()
        return Relation.equal()

    # Precond:
    #   domain is a valid domain object.
    #   info is a dictionary (no information used, but important for typing).
    #
    # Postcond:
    #   Returns a random WeightedAverage object.
    @staticmethod
    def random(domain, info):
        result = WeightedAverage(domain)
        dl = domain.length()
        result.weights = [random() for i in range(dl)]
        result.orders = [[i for i in range(domain.attr_length(j))] for j in range(dl)]
        for i in range(len(result.orders)):
            shuffle(result.orders[i])
        total = 0.0
        for weight in result.weights:
            total += weight*weight
        total = math.sqrt(total)
        for i in range(len(result.weights)):
            result.weights[i] = result.weights[i]/total
        return result

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified RPF
    @staticmethod
    def pill_label(domain, info):
        return 'WA;'+ str(domain.length()) +';'+ str(domain.attr_length_largest())


    # Precond:
    #   lines is a list of lines which represent a WeightedAverage object.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns the parsed WeightedAverage object.
    @staticmethod
    def parse(lines, domain):
        result = WeightedAverage(domain)
        for line in lines:
            line = line.strip()
            if line[0] == 'P':
                line = line.split(' ')
                result.weights.append(float(line[1]))
                order = line[2].split(',')
                order = list(map(lambda x: int(x), order))
                result.orders.append(order)
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "WA"

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the WeightedAverage object.
    def __str__(self):
        result = str(self.domain) + "\n"
        for i in range(len(self.weights)):
            order = ','.join(list(map(lambda x: str(x),self.orders[i])))
            result += ' '.join((['P',str(self.weights[i]),order,"\n"]))
        return result
