# File: alternative.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines an alternative from a specified combinatorial domain.
# Notes:
#   Alternative attribute values begin with 1, not 0.


class Alternative:
    # Precond:
    #   values is a list of integers represent the values of attributes in the
    #       alternative.
    #   domain is a valid Domain object, or None.
    #
    # Postcond:
    #   Builds a new Alternative object with the specified domain and attribute
    #   values.
    def __init__(self, values, domain=None):
        self.values = values[:]
        self.domain = domain

    # Precond:
    #   index is an integer representing the attribute index.
    #
    # Postcond:
    #   Returns the requested value.
    def value(self, index):
        return self.values[index]

    # Precond:
    #   index is an integer representing the attribute index.
    #   value is an integer represent the new value of the attribute.
    #
    # Postcond:
    #   Changes the value of the specified index to the specfied value.
    #   Returns the new value at that index.
    def set(self, index, value):
        self.values[index] = value
        return self.values[index]

    # Precond:
    #   domain is a valid Domain object, or None.
    #
    # Postcond:
    #   Return true if the alternative fits the provided domain.
    #   If the domain fits and the domain field is None then the alternative
    #   sets its domain field to the given domain.
    def matches(self, domain):
        if domain is None:
            return False
        if domain.length() != len(self.values):
            return False
        for i in range(domain.length()):
            if self.values[i] < 1 or self.values[i] > domain.attr_length(i):
                return False
        if self.domain is None:
            self.domain = domain
        return True

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the length of the alternative.
    def length(self):
        return len(self.values)

    # Precond:
    #   line is a valid string.
    #   domain is a valid Domain object or None.
    #
    # Postcond:
    #   Parses the string into an Alternative object.
    #   If parseing fails None is returned.
    #   See example_set_file_specification.md for details.
    @staticmethod
    def parse(line, domain=None):
        line = line.strip()
        contents = line.split(',')
        contents = list(map(lambda x: int(x), contents))
        return Alternative(contents, domain)

    # Precond:
    #   other is a valid Alternative instance.
    #
    # Postcond:
    #   Returns true if the alternatives are the same.
    def __eq__(self, other):
        if len(self.values) != len(other.values):
            return False
        for i in range(len(self.values)):
            if self.values[i] != other.values[i]:
                return False
        return True


    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string representation of the alternative.
    def __str__(self):
        str_vals = list(map(lambda x: str(x), self.values))
        return ','.join(str_vals)
