# File: pref_logic.py
# Author: Michael Huelsman
# Created On: 11 Dec 2019
# Purpose:
#   To provide classes for dealing with preferences specfied using formal logic.

import random
import sys, os

class PrefLiteral:
    # Precond:
    #   attr is the attribute the literal is associated with.
    #   value is the value of the attribute the literal is associated with.
    #   negated is True if the literal is a negated literal.
    #
    # Postcond:
    #   Builds a new PrefLiteral oject.
    def __init__(self, attr, value, negated=False):
        self.attr = attr
        self.value = value
        self.negated = negated

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the associated attribute.
    def getAttr(self):
        return self.attr

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the associated value of the associated attribute.
    def getValue(self):
        return self.value

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns true if the literal is negated.
    def isNegated(self):
        return self.negated

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns true if the literal is true according to the alternative.
    #   Defaults to false in the case of failure.
    def match(self, alt):
        if self.attr >= alt.length():
            return False
        result = (alt.value(self.attr) == self.value)
        if self.negated:
            return not result
        return result

    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns a randomly generated PrefLiteral object.
    @staticmethod
    def random(domain):
        attr = random.randint(0,domain.length()-1)
        value = random.randint(1,domain.attr_length(attr))
        return PrefLiteral(attr,value,random.choice([True,False]))

    # Precond:
    #   line is a string representing a literal.
    #
    # Postcond:
    #   Returns a PrefLiteral object which is identical to the literal the given
    #   string represents.
    @staticmethod
    def parse(line):
        line = line.strip()
        negation = False
        if line[0] == '-':
            negation = True
            line = line[1:]
        line = line.strip('()')
        line = line.split(',')
        return PrefLiteral(int(line[0]),int(line[1]),negation)

    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Iterates through all possible PrefLiteral objects for the given domain.
    @staticmethod
    def each_literal(domain):
        for neg in [True,False]:
            for attr in range(domain.length()):
                for val in range(1,domain.attr_length(attr)+1):
                    yield PrefLiteral(attr,val,neg)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the literal
    def __str__(self):
        result = ""
        if self.negated:
            result += '-'
        result += ''.join(['(',str(self.attr),',',str(self.value),')'])
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   returns a string for use in a neighborhood graph.
    def node_str(self):
        if(self.negated):
            return '-' + str(self.attr) + ':' + str(self.value)
        return str(self.attr) + ':' + str(self.value)

    # Precond:
    #   other is a valid PrefLiteral object.
    #
    # Postcond:
    #   Returns True if the two literals are identical.
    def __eq__(self, other):
        return (self.attr == other.attr and self.value == other.value and self.negated == other.negated)

class PrefFormula:
    # Precond:
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Builds an empty preference formula object.
    def __init__(self, domain):
        self.domain = domain
        self.clauses = 0
        self.lit_per_clause = 0
        self.literals = []

    # Precond:
    #   alt is a valid alternative.
    #
    # Postcond:
    #   Returns true if the alternative satisfies the formula, according to a
    #   CNF evaluation.
    #   Defaults to True
    def eval_CNF(self, alt):
        clause = False
        clauseIndex = 0
        for i in range(self.clauses):
            clause = False
            clauseIndex = i*self.lit_per_clause
            for j in range(self.lit_per_clause):
                if self.literals[clauseIndex + j].match(alt):
                    clause = True
                    break
            if not clause:
                return False
        return True

    # Precond:
    #   alt is a valid alternative.
    #
    # Postcond:
    #   Returns true if the alternative satisfies the formula, according to a
    #   DNF evaluation.
    #   Defaults to False
    def eval_DNF(self, alt):
        clause = True
        clauseIndex = 0
        for i in range(self.clauses):
            clause = True
            clauseIndex = i*self.lit_per_clause
            for j in range(self.lit_per_clause):
                if not self.literals[clauseIndex + j].match(alt):
                    clause = False
                    break
            if clause:
                return True
        return False


    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random PrefFormula that is a neighbor to this PrefFormula.
    def random_neighbor(self):
        result = PrefFormula(self.domain)
        result.clauses = self.clauses
        result.lit_per_clause = self.lit_per_clause
        lit_size = self.clauses*self.lit_per_clause
        lit_change = random.randint(0,lit_size-1)
        for i in range(len(self.literals)):
            if i != lit_change:
                result.literals.append(self.literals[i])
            else:
                lit_mod = PrefLiteral.random(self.domain)
                while lit_mod == self.literals[i]:
                    lit_mod = PrefLiteral.random(self.domain)
                result.literals.append(lit_mod)
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through all neighbors of the given PrefFormula
    def neighbors(self):
        for i in range(len(self.literals)):
            for lit in PrefLiteral.each_literal(self.domain):
                if lit == self.literals[i]:
                    continue
                # create new object and copy over.
                temp = PrefFormula(self.domain)
                temp.clauses = self.clauses
                temp.lit_per_clause = self.lit_per_clause
                temp.literals.extend(self.literals)
                temp.literals[i] = lit
                yield temp

    # Precond:
    #   clauses is the number of clauses to generate.
    #   lits_per_clause is the number of literals per clause.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Builds a random preference formula.
    @staticmethod
    def random(clauses, lit_per_clause, domain):
        result = PrefFormula(domain)
        result.clauses = clauses
        result.lit_per_clause = lit_per_clause
        lit_size = clauses*lit_per_clause
        result.literals = [PrefLiteral.random(domain) for i in range(lit_size)]
        return result

    # Precond:
    #   clauses is the number of clauses to generate.
    #   lits_per_clause is the number of literals per clause.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Enumerates each possible preference formula.
    @staticmethod
    def each(clauses, lit_per_clause, domain):
        result = PrefFormula(domain)
        result.clauses = clauses
        result.lit_per_clause = lit_per_clause
        lit_size = clauses*lit_per_clause
        result.literals = [None for i in range(lit_size)]
        for form in PrefFormula._possible(result, domain, lit_size, 0):
            yield form

    @staticmethod
    def _possible(current, domain, literals, literal):
        for lit in PrefLiteral.each_literal(domain):
            current.literals[literal] = lit
            if literal == literals-1:
                yield current
            else:
                for form in PrefFormula._possible(current, domain, literals, literal+1):
                    yield form

    # Precond:
    #   line is a string representing a logical formula.
    #   domain is a valid Domain object.
    #
    # Postcond:
    #   Returns a PrefFormula object which is identical to that represented by
    #   the given string.
    @staticmethod
    def parse(line, domain):
        line = line.strip()
        result = PrefFormula(domain)
        line = line.split(' ')
        result.clauses = line[0]
        result.lit_per_clause = line[1]
        line = line[2:]
        for literal in line:
            result.literals.append(PrefLiteral.parse(literal))
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the formula
    def __str__(self):
        result = str(self.clauses) + ' ' + str(self.lit_per_clause) + ' '
        result += ' '.join(list(map(lambda x: str(x),self.literals)))
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   returns a string for use in a neighborhood graph.
    def node_str(self):
        ns_func = lambda x: x.node_str()
        return ','.join(list(map(ns_func,self.literals)))
