# File: answer_set_optimization.py
# Author: Michael Huelsman
# Created On: 20 May 2020
# Purpose:
#   Contains a class which holds operations for dealing with ASO
#   preferences (assuming the generator program simply returns the set of all
#   alternatives in a given combinatorial domain).

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from utility.pref_logic import PrefFormula
from examples.relation import Relation
from random import randint

class ASO:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns an empty ASO object.
    def __init__(self, domain):
        self.domain = domain
        self.ranks = []

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the satisfaction vector of the alternative assuming DNF formulas.
    #   Defaults to returning # of ranks +1 for each formula..
    def eval_DNF(self, alt):
        result = [[len(self.ranks[i][j])+1 for j in range(len(self.ranks[i]))] for i in range(len(self.ranks))]
        if not alt.matches(self.domain):
            return result
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                for k in range(len(self.ranks[i][j])):
                    if self.ranks[i][j][k].eval_DNF(alt):
                        result[i][j] = k+1
                        break
        return result

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the satisfaction vector of the alternative assuming CNF formulas.
    #   Defaults to returning # of ranks +1 for each formula..
    def eval_CNF(self, alt):
        result = [[len(self.ranks[i][j])+1 for j in range(len(self.ranks[i]))] for i in range(len(self.ranks))]
        if not alt.matches(self.domain):
            return result
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                for k in range(len(self.ranks[i][j])):
                    if self.ranks[i][j][k].eval_CNF(alt):
                        result[i][j] = k+1
                        break
        return result

    # Precond:
    #   alt1 is a valid Alternative object.
    #   alt2 is a valud Alternative object.
    #   dnf is a boolean which is true when DNF evaluation is used.
    #
    # Postcond:
    #   Returns the relation between alt1 and alt2.
    def compare(self, alt1, alt2, dnf=True):
        satVecs = [[],[]]
        if dnf:
            satVecs[0] = self.eval_DNF(alt1)
            satVecs[1] = self.eval_DNF(alt2)
        else:
            satVecs[0] = self.eval_CNF(alt1)
            satVecs[1] = self.eval_CNF(alt2)
        for i in range(len(self.ranks)):
            result = self._pareto(satVecs[0][i],satVecs[1][i])
            if result != Relation.equal():
                return result
        return Relation.equal()

    # Precond:
    #   sVec1 is a list of integers.
    #   sVec2 is a list of integers.
    #
    # Postcond:
    #   Returns the relation between the two satisfaction vectors based on
    #   Pareto dominance.
    def _pareto(self, sVec1, sVec2):
        if len(sVec1) != len(sVec2):
            return Relation.incomparable()
        result = Relation.equal()
        for i in range(len(sVec1)):
            if result == Relation.equal():
                if sVec1[i] < sVec2[i]:
                    result = Relation.strict_preference()
                elif sVec2[i] < sVec1[i]:
                    result = Relation.strict_dispreference()
            elif result == Relation.strict_preference():
                if sVec2[i] < sVec1[i]:
                    return Relation.incomparable()
            elif result == Relation.strict_dispreference():
                if sVec1[i] < sVec2[i]:
                    return Relation.incomparable()
        return result


    # TODO: Implement these properly.
    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random RankingPrefFormula object which is a neighbor of this
    #   RankingPrefFormula object.
    def random_neighbor(self):
        result = self._copy()
        # Select the formula to change
        choice = randint(0,self.formula_length()-1)
        index = self.formula_index(choice)
        rank = index[0]
        rule = index[1]
        formula = index[2]
        result.ranks[rank][rule][formula] = result.ranks[rank][rule][formula].random_neighbor()
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the number of formulas in the ASO.
    def formula_length(self):
        total = 0
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                total += len(self.ranks[i][j])
        return total

    # Precond:
    #   n is an integer indicating which formula index to get.
    #
    # Postcond:
    #   Returns the index tuple (rank,rule,formula) of the formula which is the
    #   nth formula for the ASO.
    def formula_index(self, n):
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                if n >= len(self.ranks[i][j]):
                    n -= len(self.ranks[i][j])
                else:
                    return (i,j,n)
        return (0,0,0)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all neighbors of this ASO object.
    def neighbors(self):
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                for k in range(len(self.ranks[i][j])):
                    result = self._copy()
                    for neighbor in self.ranks[i][j][k].neighbors():
                        result.ranks[i][j][k] = neighbor
                    yield result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a completely separate copy of the ASO.
    def _copy(self):
        result = ASO(self.domain)
        result.ranks = [[[] for j in range(len(self.ranks[i]))] for i in range(len(self.ranks))]
        for i in range(len(self.ranks)):
            for j in range(len(self.ranks[i])):
                for k in range(len(self.ranks[i][j])):
                    result.ranks[i][j].append(self.ranks[i][j][k])
        return result



    # Precond:
    #  domain is a valid Domain object.
    #   info is a dictionary containing all needed generating information.
    #       literals: The number of literals per clause.
    #       clauses: The number of clauses per formula.
    #       formulas: The number of formulas (satisfaction ranks) per rule.
    #       rules: The number of rules per rank.
    #       ranks: The number of ranks.
    #
    # Postcond:
    #   Returns a randomly generated ASO ovject of the specified type.
    @staticmethod
    def random(domain, info):

        perm_dir = '../Asprin/Generated_Preference_Model/'
        if os.path.isdir(perm_dir):
            os.system('rm -rf ' + perm_dir)
        os.system('mkdir ' + perm_dir)
        os.system('touch ' + perm_dir + 'ASO.txt')

        result = ASO(domain)
        result.ranks = [None for i in range(info['ranks'])]
        # Generate each rank one at a time.
        for rank in range(info['ranks']):
            result.ranks[rank] = [None for i in range(info['rules'])]
            for rule in range(info['rules']):
                # Add a rule to the rank.
                result.ranks[rank][rule] = []
                for formula in range(info['formulas']):
                    # Add a random formula to the rule.
                    temp = PrefFormula.random(info['clauses'],info['literals'],domain)
                    result.ranks[rank][rule].append(temp)

        with open(perm_dir + 'ASO.txt', 'w') as file:
            file.write(str(result))
        return result

    def __str__(self):
        result = str(self.domain) + "\n"
        for rank in self.ranks:
            result += "\n"
            for rule in rank:
                for pref in rule:
                    result += ' '.join(['P', str(pref), "\n"])
        return result

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified LPM
    @staticmethod
    def pill_label(domain, info):
        des = ['ASO',str(info['literals']),str(info['clauses']),str(info['formulas']),str(info['rules']),str(info['ranks']),str(domain.length()),str(domain.attr_length_largest())]
        return ';'.join(des)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "ASO"
