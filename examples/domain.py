# File: domain.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines a combinatorial domain.
# Notes:
#

from .alternative import Alternative
from random import randint

class Domain:
    # Precond:
    #   attributes is an integer representing the number of attributes in the
    #       domain.
    #   value is a list of integers. Each entry represent the number of unique
    #       values the cooresponding attribute can take.
    #   The length of values must equal or exceed that of the value of
    #       attributes. In the case of an excess all remaining values are
    #       ignored.
    #
    # Postcond:
    #   Builds a new Domain object with the specified parameters.
    def __init__(self, attributes, value):
        self.attributes = attributes
        self.value = value[0:self.attributes]
        self.attributes = len(self.value)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the number of attributes.
    def length(self):
        return self.attributes

    # Precond:
    #   attribute is an integer representing an attribute.
    #
    # Postcond:
    #   Returns the number of values associated with the given attribute.
    #   Returns 0 if a bad attribute is given.
    def attr_length(self, attribute):
        if attribute < 0 or attribute >= self.attributes:
            return 0
        return self.value[attribute]

    # Precond:
    #
    # Postcond:
    #   Returns the number of values associated with the given largest attribute.
    #   Returns 0 if a bad attribute is given.
    def attr_length_largest(self):
        result = 0
        for item in self.value:
            if item > result:
                result = item
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a random pair of alternatives, with a canonical ordering.
    def random_pair(self):
        alt1 = Alternative([randint(1,self.value[i]) for i in range(self.attributes)])
        alt2 = Alternative([randint(1,self.value[i]) for i in range(self.attributes)])
        while alt1 == alt2:
            alt2 = Alternative([randint(1,self.value[i]) for i in range(self.attributes)])
        for i in range(self.attributes):
            if alt1.value(i) < alt2.value(i):
                return (alt1,alt2)
            elif alt1.value(i) > alt2.value(i):
                return (alt2,alt1)
        return (alt1, alt2)

    # Postcond:
    #   size is an integer indicating the number of pairs to return.
    #
    # Precond:
    #   Returns a random set of pairs, with no two pairs repeating.
    def random_pair_set(self, size):
        result = [self.random_pair() for i in range(size)]
        found = False
        while len(result) != size:
            temp = self.random_pair()
            found = True
            for pair in result:
                if pair[0] == temp[0] and pair[1] == temp[1]:
                    found = False
                    break
            if found:
                result.append(temp)
        return result


    # Precond:
    #   alt is a valid Alternative object for this domain, or None.
    #
    # Postcond:
    #   Iterator that yeilds each possible alternative in numerical order
    #   (least significant attribute first). If alt is specified then the
    #   iteration starts from that alternative.
    def each(self, alt=None):
        if alt is None:
            alt = Alternative([1 for i in range(self.attributes)])
        else:
            alt = Alternative([alt.value(i) for i in range(self.attributes)])
        if not self.is_highest(alt):
            while not self.is_highest(alt):
                yield alt
                alt = self.next_alternative(alt)
        yield alt

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterator that yeilds each possible unique pair of alternatives in
    #   numerical order (least significant attribute first).
    def each_pair(self):
        for alt1 in self.each():
            if not self.is_highest(alt1):
                for alt2 in self.each(self.next_alternative(alt1)):
                    yield (alt1,alt2)


    # Precond:
    #   alt is a valid Alternative object.
    #
    # Postcond:
    #   Returns true if alt does not have the highest possible numerical value.
    def is_highest(self, alt):
        for i in range(self.attributes):
            if(alt.value(i) < self.value[i]):
                return False
        return True

    # Precond:
    #   alt is a valid Alternative object
    #
    # Postcond:
    #   Returns the next alternativein numerical order (least significant
    #   attribute first).
    def next_alternative(self, alt):
        n_alt = Alternative([alt.value(i) for i in range(self.attributes)])
        n_alt.set(0,n_alt.value(0)+1)
        for i in range(self.attributes-1):
            if n_alt.value(i) > self.value[i]:
                n_alt.set(i,1)
                n_alt.set(i+1,n_alt.value(i+1)+1)
            else:
                return n_alt
        return n_alt

    # Precond:
    #   line is a valid string.
    #
    # Postcond:
    #   Parses the string into a domain object.
    #   If parseing fails None is returned.
    #   See example_set_file_specification.md for details.
    @staticmethod
    def parse(line):
        line = line.strip().lower()
        if line[0] != 'd':
            return None
        contents = line.split(' ')
        attrs = int(contents[1])
        values = contents[2:]
        values = list(map(lambda x: int(x),values))
        if attrs <= len(values):
            return Domain(attrs,values)
        return None

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the string representation of the domain.
    def __str__(self):
        str_vals = list(map(lambda x: str(x), self.value))
        return ' '.join(['D', str(self.attributes), ' '.join(str_vals)])
