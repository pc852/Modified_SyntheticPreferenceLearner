# File: relation.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines the set of relations between two alternatives.
# Notes:
#   Values and their meaning:
#       -2: alt2 is strictly preferred to alt1
#       -1: alt2 at least as preferred as alt1
#        0: alt1 is equally preferred to alt2
#        1: alt1 is at least as preferred as alt2
#        2: alt1 is strictly preferred to alt2
#        3: alt1 is incomparable with alt2
#   3 and -3 represent the same status

class Relation:
    # Precond:
    #   values is the comparison value of two objects.
    #
    # Postcond:
    #   Builds a new Relation object.
    #   If value is outside the bounds of the defined values above,
    #   default to 3.
    def __init__(self, value):
        if abs(value) >= 3:
            self.value = 3
        else:
            self.value = value

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the reverse relation.
    def reverse(self):
        return Relation(-self.value)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the inverse relation.
    def inverse(self):
        if self.value == -2:
            return Relation(1)
        elif self.value == -1:
            return Relation(2)
        elif self.value == 1:
            return Relation(-2)
        elif self.value == 2:
            return Relation(-2)
        else:
            return Relation(self.value)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a proper label for learning preference relations using a neural
    #   network.
    def neural_label(self):
        if self.value == -2:
            return [1.0,0.0,0.0,0.0,0.0,0.0]
        elif self.value == -1:
            return [0.0,1.0,0.0,0.0,0.0,0.0]
        elif self.value == 0:
            return [0.0,0.0,1.0,0.0,0.0,0.0]
        elif self.value == 1:
            return [0.0,0.0,0.0,1.0,0.0,0.0]
        elif self.value == 2:
            return [0.0,0.0,0.0,0.0,1.0,0.0]
        else:
            return [0.0,0.0,0.0,0.0,0.0,1.0]

    # Precond:
    #   label is a list of floating point values.
    #
    # Postcond:
    #   Builds a new relation from the given label.
    @staticmethod
    def parse_label(label):
        index = 0
        for i in range(1,len(label)):
            if label[index] < label[i]:
                index = i
        return Relation(index-2)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the relation.
    def __str__(self):
        return str(self.value)

    # Precond:
    #   line is a valid string.
    #
    # Postcond:
    #   Parses the string into a Relation object.
    #   If parseing fails None is returned.
    #   See example_set_file_specification.md for details.
    @staticmethod
    def parse(line,domain=None):
        line = line.strip()
        return Relation(int(line))

    # Precond:
    #   other is a valid Relation object.
    #
    # Postcond:
    #   Returns true if the relations are the same.
    def __eq__(self, other):
        return self.value == other.value


    # Static methods for the various relations.

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing strict dispreference.
    @staticmethod
    def strict_dispreference():
        return Relation(-2)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing dispreference.
    @staticmethod
    def dispreference():
        return Relation(-1)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing equal preference.
    @staticmethod
    def equal():
        return Relation(0)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing preference.
    @staticmethod
    def preference():
        return Relation(1)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing strict preference.
    @staticmethod
    def strict_preference():
        return Relation(2)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a Relation object representing incomparablility.
    @staticmethod
    def incomparable():
        return Relation(3)
