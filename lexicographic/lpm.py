# File: lpm.py
# Author: Michael Huelsman
# Created On: 10 Dec 2019
# Purpose:
#   Specifies a class for handling Lexicographic Preference Models.

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import random
from examples.relation import Relation
from itertools import permutations

class LPM:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Produces an new empty LPM for the given domain.
    def __init__(self,domain):
        self.domain = domain
        self.importance = []
        self.orders = []


    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Creates a randomly built LPM.
    @staticmethod
    def random(domain, info):

        perm_dir = '../Asprin/Generated_Preference_Model/'
        if os.path.isdir(perm_dir):
            os.system('rm -rf ' + perm_dir)
        os.system('mkdir ' + perm_dir)
        os.system('touch ' + perm_dir + 'lpm.txt')

        result = LPM(domain)
        result.importance = [i for i in range(domain.length())]
        random.shuffle(result.importance)
        result.orders = [[] for i in range(domain.length())]
        for i in range(domain.length()):
            result.orders[i] = [(j+1) for j in range(domain.attr_length(i))]
            random.shuffle(result.orders[i])

        with open(perm_dir + 'lpm.txt', 'w') as file:
            file.write(str(result))

        return result

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified LPM
    @staticmethod
    def pill_label(domain, info):
        return 'LPM;'+ str(domain.length()) +';'+ str(domain.attr_length_largest())

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Creates a randomly built partial LPM.
    @staticmethod
    def random_partial(domain, info):
        result = LPM(domain)
        result.importance = [i for i in range(domain.length())]
        random.shuffle(result.importance)
        partial_point = random.randint(1,domain.length())
        result.importance = result.importance[:partial_point]
        result.orders = [[] for i in range(domain.length())]
        for i in range(domain.length()):
            result.orders[i] = [(j+1) for j in range(domain.attr_length(i))]
            random.shuffle(result.orders[i])

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random LPM object which is a neighbor of this LPM object.
    def random_neighbor(self):
        result = LPM(self.domain)
        result.orders.extend(self.orders)
        result.importance.extend(self.importance)
        if random.random() <= 0.5:
            swap_index = random.randint(0,len(result.importance)-2)
            sw = result.importance[swap_index]
            result.importance[swap_index] = result.importance[swap_index+1]
            result.importance[swap_index+1] = sw
        else:
            order_swap = random.randint(0,len(result.orders)-1)
            swap_index = random.randint(0,len(result.orders[order_swap])-2)
            sw = result.orders[order_swap][swap_index]
            result.orders[order_swap][swap_index] = result.orders[order_swap][swap_index+1]
            result.orders[order_swap][swap_index+1] = sw
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all neighbors of this LPM object.
    def neighbors(self):
        for i in range(len(self.importance)-1):
            temp = LPM(self.domain)
            temp.orders.extend(self.orders)
            temp.importance.extend(self.importance)
            sw = temp.importance[i]
            temp.importance[i] = temp.importance[i+1]
            temp.importance[i+1] = sw
            yield temp
        for i in range(len(self.orders)):
            for j in range(len(self.orders[i])-1):
                temp = LPM(self.domain)
                temp.orders.extend(self.orders)
                temp.importance.extend(self.importance)
                sw = temp.orders[i][j]
                temp.orders[i][j] = temp.orders[i][j+1]
                temp.orders[i][j+1] = sw
                yield temp

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
        for attr in self.importance:
            v1 = alt1.value(attr)
            v2 = alt2.value(attr)
            if v1 != v2:
                if self.orders[attr].index(v1) < self.orders[attr].index(v2):
                    return Relation.strict_preference()
                else:
                    return Relation.strict_dispreference()
        return Relation.equal()


    # Precond:
    #   lines is a set of strings which specifies an LPM.
    #   domain is the domain of the LPM described by the lines.
    #
    # Postcond:
    #   Returns the LPM specified by the given lines.
    @staticmethod
    def parse(lines, domain):
        result = LPM()
        result.domain = domain
        result.orders = [[] for i in range(domain.length())]
        convertList = lambda x: list(map(lambda y: int(y), x))
        for line in lines:
            line = line.strip()
            if line[0] == 'I':
                line = line.split(' ')[1:]
                result.importance = convertList(line)
            elif line[0] == 'P':
                line = line.split(' ')[1:]
                order = int(line[0])
                result.orders[order] = convertList(line[1:])
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "LPM"

    # Precond:
    #   None.
    # Postcond:
    #   Builds a string representation of the LPM.
    def __str__(self):
        result = str(self.domain)+"\n"
        result += 'I '
        result += ' '.join(list(map(lambda x: str(x), self.importance))) + "\n"
        for i in range(len(self.orders)):
            result += 'P ' + str(i) + ' ' + ' '.join(list(map(lambda x: str(x), self.orders[i]))) + "\n"
        return result

    # Precond:
    #   ex_set is a valid ExampleSet object.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns an LPM learned from the ExampleSet
    @staticmethod
    def learn_greedy(ex_set, domain):
        ex_set.unflag_all()
        for ex in ex_set.each_unflagged():
            if ex.get_relation() == Relation.equal():
                ex.flag()
        importance = []
        orders = [[j+1 for j in range(domain.attr_length(i))] for i in range(domain.length())]
        possible_next = [i for i in range(domain.length())]
        while len(possible_next) != 0:
            best_attr = possible_next[0]
            best_score = -1
            best_order = [i+1 for i in range(domain.attr_length(best_attr))]
            for attr in possible_next:
                values = [i+1 for i in range(domain.attr_length(attr))]
                for order in permutations(values,len(values)):
                    incorrect = 0
                    for ex in ex_set.each_unflagged():
                        if ex.get_alts()[0].value(attr) == ex.get_alts()[1].value(attr):
                            continue
                        rank1 = order.index(ex.get_alts()[0].value(attr))
                        rank2 = order.index(ex.get_alts()[1].value(attr))
                        if ex.get_relation() == Relation.strict_preference():
                            if rank1 > rank2:
                                incorrect += 1
                        if ex.get_relation() == Relation.strict_dispreference():
                            if rank1 < rank2:
                                incorrect += 1
                    if best_score == -1 or incorrect < best_score:
                        best_score = incorrect
                        best_attr = attr
                        best_order = order[:]
            importance.append(best_attr)
            orders[best_attr] = best_order
            possible_next.remove(best_attr)
            for ex in ex_set.each_unflagged():
                if ex.get_alts()[0].value(best_attr) != ex.get_alts()[1].value(best_attr):
                    ex.flag()
        result = LPM(domain)
        result.importance = importance
        result.orders = orders
        return result

    # Precond:
    #   ex_set is a valid ExampleSet object.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns an LPM learned from the ExampleSet in a Maximin manner
    @staticmethod
    def learn_greedy_maximin(ex_set, domain):
        ex_set.unflag_all()
        for ex in ex_set.each_unflagged():
            if ex.get_relation() == Relation.equal():
                ex.flag()
        importance = []
        orders = [[j+1 for j in range(domain.attr_length(i))] for i in range(domain.length())]
        possible_next = [i for i in range(domain.length())]
        agents = ex_set.get_agents()
        while len(possible_next) != 0:
            best_attr = possible_next[0]
            best_score = -1
            best_order = [i+1 for i in range(domain.attr_length(best_attr))]
            for attr in possible_next:
                values = [i+1 for i in range(domain.attr_length(attr))]
                for order in permutations(values,len(values)):
                    agent_counts = {}
                    for agent in agents:
                        agent_counts[agent] = 0
                    for ex in ex_set.each_unflagged():
                        if ex.get_alts()[0].value(attr) == ex.get_alts()[1].value(attr):
                            continue
                        rank1 = order.index(ex.get_alts()[0].value(attr))
                        rank2 = order.index(ex.get_alts()[1].value(attr))
                        if ex.get_relation() == Relation.strict_preference():
                            if rank1 > rank2:
                                agent_counts[ex.get_agent()] += 1
                        if ex.get_relation() == Relation.strict_dispreference():
                            if rank1 < rank2:
                                agent_counts[ex.get_agent()] += 1
                    incorrect = 0
                    for _, count in agent_counts.items():
                        if count > incorrect:
                            incorrect = count
                    if best_score == -1 or incorrect < best_score:
                        best_score = incorrect
                        best_attr = attr
                        best_order = order[:]
            importance.append(best_attr)
            orders[best_attr] = best_order
            possible_next.remove(best_attr)
            for ex in ex_set.each_unflagged():
                if ex.get_alts()[0].value(best_attr) != ex.get_alts()[1].value(best_attr):
                    ex.flag()
        result = LPM(domain)
        result.importance = importance
        result.orders = orders
        return result
