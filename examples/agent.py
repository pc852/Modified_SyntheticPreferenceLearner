# File: agent.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines an example generating agent.
# Notes:

from .example import Example

class Agent:
    nextID = 1
    # Precond:
    #   model is an object which has the following methods:
    #       compare(obj1: Alternative, obj2: Alternative): Relation.
    #       str(): String
    #   domain is a valid Domain object or None.
    #
    # Postcond:
    #   Builds a new Agent object.
    def __init__(self,model,domain=None):
        self.id = Agent.nextID
        Agent.nextID += 1
        self.model = model
        self.domain = domain

    # Precond:
    #   alt1 is a valid Alternative object.
    #   alt2 is a valid Alternative object.
    #
    # Postcond:
    #   Returns an example based on the agent's model.
    def build_example(self, alt1, alt2):
        relation = self.model.compare(alt1,alt2)
        return Example(alt1,alt2,relation,self.domain,self.id)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string version of the agent.
    def __str__(self):
        return ' '.join([str(self.id),str(self.model)])
