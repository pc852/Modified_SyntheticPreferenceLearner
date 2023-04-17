# File: ranking_formula.py
# Author: Michael Huelsman
# Created On: 12 Dec 2019
# Purpose:
#   Define a ranking preference formula.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from utility.pref_logic import PrefFormula
from examples.relation import Relation
from random import randint

class RankingPrefFormula:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Builds a new empty RankingPrefFormula object.
    def __init__(self, domain):
        self.domain = domain
        self.ranks = []

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the number of ranks in the RankingPrefFormula object.
    def length(self):
        return len(self.ranks)

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the first rank where the alternative matches the DNF formula.
    #   Defaults to returning # of ranks + 1.
    def eval_DNF(self, alt):
        if not alt.matches(self.domain):
            return len(self.ranks)+1
        for i in range(len(self.ranks)):
            if self.ranks[i].eval_DNF(alt):
                return i+1
        return len(self.ranks)+1

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the first rank where the alternative matches the CNF formula.
    #   Defaults to returning # of ranks + 1.
    def eval_CNF(self, alt):
        if not alt.matches(self.domain):
            return len(self.ranks)+1
        for i in range(len(self.ranks)):
            if self.ranks[i].eval_CNF(alt):
                return i+1
        return len(self.ranks)+1

    # Precond:
    #   alt1 is a valid Alternative object.
    #   alt2 is a valud Alternative object.
    #   dnf is a boolean which is true when DNF evaluation is used.
    #
    # Postcond:
    #   Returns the relation between alt1 and alt2.
    def compare(self, alt1, alt2, dnf=False):
        rank1 = rank2 = 0
        if dnf:
            rank1 = self.eval_DNF(alt1)
            rank2 = self.eval_DNF(alt2)
        else:
            rank1 = self.eval_CNF(alt1)
            rank2 = self.eval_CNF(alt2)
        if rank1 < rank2:
            return Relation.strict_dispreference()
        elif rank1 > rank2:
            return Relation.strict_preference()
        return Relation.equal()

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random RankingPrefFormula object which is a neighbor of this
    #   RankingPrefFormula object.
    def random_neighbor(self):
        result = RankingPrefFormula(self.domain)
        # Select the formula to change
        formula = randint(0,len(self.ranks)-1)
        for i in range(len(self.ranks)):
            if i != formula:
                result.ranks.append(self.ranks[i])
            else:
                result.ranks.append(self.ranks[i].random_neighbor())
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all neighbors of this RankingPrefFormula object.
    def neighbors(self):
        for i in range(len(self.ranks)):
            for form in self.ranks[i].neighbors():
                temp = RankingPrefFormula(self.domain)
                temp.ranks.extend(self.ranks)
                temp.ranks[i] = form
                yield temp

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary with the following keys:
    #       clauses is the number of clauses per rank.
    #       literals is the number of literals per clause.
    #       ranks is the number of ranks to generate.
    #
    # Postcond:
    #   Returns a random RankingPrefFormula object.
    @staticmethod
    def random(domain, info):

        perm_dir = '../Asprin/Generated_Preference_Model/'
        if os.path.isdir(perm_dir):
            os.system('rm -rf ' + perm_dir)
        os.system('mkdir ' + perm_dir)
        os.system('touch ' + perm_dir + 'RPF.txt')

        result = RankingPrefFormula(domain)
        for i in range(info['ranks']):
            result.ranks.append(PrefFormula.random(info['clauses'],info['literals'],domain))

        with open(perm_dir + 'RPF.txt', 'w') as file:
            file.write(str(result))

        return result

    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary with the following keys:
    #       clauses is the number of clauses per rank.
    #       literals is the number of literals per clause.
    #       ranks is the number of ranks to generate
    #
    # Postcond:
    #   Enmuerates all possible RPFs given info and domain.
    @staticmethod
    def each(domain, info):
        temp = RankingPrefFormula(domain)
        temp.ranks = [None for i in range(info['ranks'])]
        for rpf in RankingPrefFormula._possible(temp, domain, info, 0):
            yield rpf

    @staticmethod
    def _possible(current, domain, info, rank):
        for form in PrefFormula.each(info['clauses'],info['literals'],domain):
            current.ranks[rank] = form
            if rank == info['ranks']-1:
                yield current
            else:
                for rpf in RankingPrefFormula._possible(current, domain, info, rank+1):
                    yield rpf




    # Precond:
    #   domain is a valid Domain object.
    #   info is a valid dictionary (data unused, but important for typing).
    #
    # Postcond:
    #   Returns a pill string describing the specified RPF
    @staticmethod
    def pill_label(domain, info):
        info_str = ';'.join([str(info['clauses']),str(info['literals']),str(info['ranks'])])
        return info_str+';RPF;'+ str(domain.length()) +';'+ str(domain.attr_length_largest())

    # Precond:
    #   lines is a list strings representing rank formulas (in order).
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns a RankingPrefFormula object.
    @staticmethod
    def parse(lines, domain):
        result = RankingPrefFormula(domain)
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if lines[i][0] == 'P':
                lines[i] = lines[i][1:]
                result.ranks.append(PrefFormula.parse(lines[i],domain))

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string identifier of this class.
    @staticmethod
    def string_id():
        return "RPF"

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the ranking formula.
    def __str__(self):
        result = str(self.domain) + "\n"
        for i in range(len(self.ranks)):
            result += ' '.join(['P', str(self.ranks[i]), "\n"])
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a unique string which is not easily parsable ofr use in a
    #   neighborhood evaluation graph.
    def node_str(self):
        ns_func = lambda x: x.node_str()
        return ';'.join(list(map(ns_func,self.ranks)))
