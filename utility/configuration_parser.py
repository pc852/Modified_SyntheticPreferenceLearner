# File: configuration_parser.py
# Author: Michael Huelsman
# Created On: 10 March 2020
# Purpose:
#   Handles parsing and storage of configuration files for the generation
#   of synthetic preferences.

import sys, os
sys.path.insert(0, os.path.abspath('..'))
from examples.domain import Domain

# Holds data for a single agent.
class AgentHolder:
    # Precond:
    #   type is a string identifying the type of agent.
    #   size is the number of examples the agent will produce.
    #   info is a dictionary containing additional information.
    #
    # Postcond:
    #   Builds a new AgentHolder object.
    def __init__(self, type, size, info):
        self.type = type
        self.size = size
        self.info = info

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a string representation of the agent holder.
    def __str__(self):
        result = "AGENT\n"
        result += "\ttype: " + self.type + "\n"
        result += "\tsize: " + str(self.size) + "\n"
        for item in self.info:
            result += "\t" + str(item) + ": " + str(self.info[item]) + "\n"
        result += "END\n"
        return result

# Precond:
#   filename is the name of a valid configuration file.
#
# Postcond:
#   Returns a tuple containing, in order, these items:
#    1) Domain object.
#    2) List of AgentHolder objects.
#    3) True/False Flag indicating success/failure.
#    4) Error Message
def parse_configuration(filename):
    domain = None
    agents = []
    line = ''
    contents = []
    with open(filename,'r') as fin:
        line = fin.readline()
        while(line != ''):
            line = line.strip().lower()
            if line == '':
                line = fin.readline()
                continue
            elif line[0] != '#':
                if line[0] == 'd':
                    domain = Domain.parse(line)
                elif line == 'agent':
                    info = {}
                    type = None
                    size = 0
                    line = fin.readline().strip().lower()
                    while(line != 'end'):
                        if line[0] == '#' or line == '':
                            line = fin.readline()
                            if(line == ''):
                                return (None,[],False,"Missing End for agent " + str(len(agents)+1))
                            line = line.strip().lower()
                            continue
                        contents = line.split(':')
                        contents = list(map(lambda x: x.strip(), contents))
                        if contents[0] == 'type':
                            type = contents[1]
                        elif contents[0] == 'size':
                            size = int(contents[1])
                        else:
                            info[contents[0]] = int(contents[1])
                        line = fin.readline()
                        if(line == ''):
                            return (None,[],False,"Missing End for agent " + str(len(agents)+1))
                        line = line.strip().lower()
                    agents.append(AgentHolder(type, size, info))
            line = fin.readline()
    if domain is None:
        return (None,[],False, 'No domain specified.')
    return (domain,agents, True, "Success.")
