# File: preference_condition.py
# Author: Michael Huelsman
# Created On: 20 Feb 2020
# Purpose:
#   Contains general classes for dealing with conditional preferences.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from examples.relation import Relation
from random import shuffle

# Class for handling a single alternative condition.
class Condition:
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds an empty condition (vacuously true).
    def __init__(self):
        self.literals = []

    # Precond:
    #   attr is an attribute.
    #   val is a valid value for attr to have.
    #
    # Postcond:
    #   Adds the attribute value pair as a positive literal.
    def add_positive(self,attr,val):
        self.literals.append((attr,val))

    # Precond:
    #   attr is an attribute.
    #   val is a valid value for attr to have.
    #
    # Postcond:
    #   Adds the attribute value pair as a negative literal.
    def add_negative(self,attr,val):
        self.literals.append((attr,-val))

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns true if the alternative satisfies the condition.
    def matches(self,alt):
        for lit in self.literals:
            if lit[1] < 0:
                if alt.value(lit[0]) == abs(lit[1]):
                    return False
            else:
                if alt.value(lit[0]) != lit[1]:
                    return False
        return True

    # Precond:
    #   literal is a pair of values.
    #
    # Postcond:
    #   Returns a string representation of the given literal.
    def _literal_string(self,literal):
        return str(literal[0])+'.'+str(literal[1])

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the condition.
    def __str__(self):
        str_lits = list(map(lambda x: self._literal_string(x),self.literals))
        return ','.join(str_lits)

    # Precond:
    #   line is a string representing a literal.
    #
    # Postcond:
    #   Returns the parsed literal.
    @staticmethod
    def _parse_literal(line):
        return tuple(map(lambda x: int(x),line.split('.')))

    # Precond:
    #   line is a string describing a condition.
    #
    # Postcond:
    #   Returns the Condition object specified by line.
    @staticmethod
    def parse(line):
        line = line.strip().split(',')
        lits = map(Condition._parse_literal,line)






# Class for handling a single conditional preference entry
class ConditionalPreference:
    # Precond:
    #   cond is a valid Condition object.
    #   order is a list of domain value from most preferred[0] to least.
    #
    # Postcond:
    #   Builds a new ConditionalPreference object.
    def __init__(self,cond,order):
        self.condition = cond
        self.order = order

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns true if the condition is satified by the alternative.
    def matches(self,alt):
        return self.condition.matches(alt)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the associated order.
    def get_order(self):
        return self.order

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the conditional preference.
    def __str__(self):
        ord = ','.join(list(map(lambda x: str(x),self.order)))
        return str(self.condition) + ';' + ord

    # Precond:
    #  line is a string representing a conditional preference.
    #
    # Postcond:
    #  Returns the ConditionalPreference object specfied by line.
    @staticmethod
    def parse(line):
        line = line.strip().split(';')
        order = list(map(lambda x: int(x),line[1].split(',')))
        cond = Condition.parse(line[0])
        return ConditionalPreference(cond,order)

    # Precond:
    #   conv is a valid CPYnet_CondPref object.
    #   num is an array of all attributes.
    #   convers is a list of lists containing canconicalized values.
    #   over is the attribute being converted.
    #
    # Postcond:
    #   Coverts the given conv into a SimpleCondPref object and stores it in
    #   this object.
    @staticmethod
    def convert_CPYNet(conv, num, convers, over):
        cond_dict = conv.pref[0]
        order = []
        cond = Condition()
        # Convert the condition itself
        for attr in conv.pref[0].keys():
            converted = convers[num.index(attr)].index(conv.pref[0][attr])+1
            cond.add_positive(num.index(attr),converted)
        # Convert the preference list.
        for val in conv.pref[1]:
            order.append(convers[num.index(over)].index(val)+1)
        return ConditionalPreference(cond,order)

# Class for building and handling CPTs
class CPT:
    # Precond:
    #   attr is the attribute this CPT is associated with.
    #
    # Postcond:
    #   Builds a new blank CPT.
    def __init__(self, attr):
        self.attr = attr
        self.preferences = []

    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns the preference order over the domain of the attribute.
    #   Return None if no matching preference is found.
    def order(self, alt):
        for pref in self.preferences:
            if pref.matches(alt):
                return pref.get_order()
        return None

    # Precond:
    #   alt1 is a valud Alternative object.
    #   alt2 is a valid Alternative object.
    #
    # Postcond:
    #   Compares the two alternatives based on the CPTs attribute and
    #   whichever condition is satisfied by alt1.
    #   Returns the incomparable relation if a problem occurred.
    def compare(self, alt1, alt2):
        pref = self.order(alt1)
        v1,v2 = alt1.value(self.attr),alt2.value(self.attr)
        if v1 not in pref or v2 not in pref:
            return Relation.equal()
        r1,r2 = pref.index(v1),pref.index(v2)
        if r1 < r2:
            return Relation.strict_preference()
        elif r1 > r2:
            return Relation.strict_dispreference()
        else:
            return Realtion.equal()

    # Precond:
    #   pref is a valid ConditionalPreference object.
    #
    # Postcond:
    #   Adds pref to the end of the preferences list.
    def add_entry(self, pref):
        self.preferences.append(pref)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Converts the CPT into a string.
    def __str__(self):
        entries = '|'.join(list(map(lambda x: str(x),self.preferences)))
        return str(self.attr)+'|'+entries

    # Precond:
    #   domain ia a valid domain object.
    #   conditions is a list of integers indicating which attributes condition
    #       the attribute.
    #   attr is the attribute over which preferences are specfied.
    #
    # Postcond:
    #   Returns a randomly generated CPT.
    @staticmethod
    def random(domain, conditions, attr):
        result = CPT(attr)
        if len(conditions) == 0:
            order = [i+1 for i in range(domain.attr_length(attr))]
            shuffle(order)
            result.add_entry(ConditionalPreference(Condition(),order))
        else:
            for value in result._count(domain, conditions):
                cond = Condition()
                for i in range(len(conditions)):
                    cond.add_positive(conditions[i],value[i])
                order = [i+1 for i in range(domain.attr_length(attr))]
                shuffle(order)
                result.add_entry(ConditionalPreference(cond,order))
        return result

    # Precond:
    #   domain ia a valid domain object.
    #   attr is a list of attributes.
    #
    # Postcond:
    #   Enumerates through all combinations of values over the attirbutes.
    def _count(self, domain, attr):
        values = [1 for i in range(len(attr))]
        while values[-1] <= domain.attr_length(attr[-1]):
            yield values
            values[0] += 1
            for i in range(0,len(attr)-1):
                if values[i] <= domain.attr_length(attr[i]):
                    break
                else:
                    values[i] = 1
                    values[i+1] += 1


    # Precond:
    #   line is a string representing a CPT.
    #
    # Postcond:
    #   Returns a new CPT object based on the line given.
    @staticmethod
    def parse(line):
        line = line.strip().split('|')
        attr = int(line[0])
        result = CPT(attr)
        line = line[1:]
        pref = list(map(lambda x: ConditionalPreference.parse(x),line))
        result.preferences = pref
        return result
