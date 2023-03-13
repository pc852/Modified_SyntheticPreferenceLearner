# File: example.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines an example between two alternatives in a combinatorial domain.
# Notes:
#   An example should be immutable for the most part.

from .alternative import Alternative
from .relation import Relation

class Example:
    # Precond:
    #   alt1 is a valid Alternative object.
    #   alt2 is a valid Alterantive object.
    #   relation is a valid Relation object.
    #   domain is a valid Domain object.
    #   agent is a valid Agent ID integer.
    #
    # Postcond:
    #   Builds a new Example object.
    def __init__(self, alt1, alt2, relation, domain=None, agent=None):
        self.pair = (alt1,alt2)
        self.relation = relation
        self.domain = domain
        self.agent = agent
        self.flagged = False


    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the ordered pair of alternatives.
    def get_alts(self):
        return self.pair

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the relation.
    def get_relation(self):
        return self.relation

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the agent who made the example.
    def get_agent(self):
        return self.agent

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the domain of the example.
    def get_domain(self):
        return self.domain

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns True if the example has been flagged.
    def is_flagged(self):
        return self.flagged

    # Precond:
    #   None.
    #
    # Postcond:
    #   Flags the example.
    def flag(self):
        self.flagged = True

    # Precond:
    #   None.
    #
    # Postcond:
    #   Unflags the example.
    def unflag(self):
        self.flagged = False



    # Precond:
    #   other is a valid Example object.
    #
    # Postcond:
    #   Returns true if the examples are identical.
    #   ONLY compares alterantives and the relation.
    def __eq__(self,other):
        if self.pair[0] == other.pair[0] and self.pair[1] == other.pair[1]:
            return self.relation == other.relation
        elif self.pair[0] == other.pair[1] and self.pair[1] == other.pair[0]:
            return self.relation == other.relation.reverse()
        else:
            return False

    # Precond:
    #   line is a valid string.
    #   domain is a valid Domain object or None.
    #
    # Postcond:
    #   Parses the string into an Example object.
    #   If parseing fails None is returned.
    #   See example_set_file_specification.md for details.
    @staticmethod
    def parse(line,domain=None):
        line = line.strip().lower()
        if line[0] != 'e':
            return None
        contents = line.split(' ')
        contents = contents[1:]
        if len(contents) < 3:
            return None
        alt1 = Alternative.parse(contents[0])
        alt2 = Alternative.parse(contents[1])
        relation = Relation.parse(contents[2])
        agent = None
        if len(contents > 3):
            agent = int(contents[3])
        return Example(alt1,alt2,relation,agent,domain)

    # Precond:
    #  None.
    #
    # Postcond:
    #   Returns a string representation of the example.
    def __str__(self):
        substrs = ['e', str(self.pair[0]), str(self.pair[1])]
        substrs.append(str(self.relation))
        substrs.append(str(self.agent))
        return ' '.join(substrs)
