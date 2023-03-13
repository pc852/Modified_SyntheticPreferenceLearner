# File: example_set.py
# Author: Michael Huelsman
# Created On: 23 Oct 2019
# Purpose:
#   Defines an example set.
# Notes:
#   Updated on 25 Oct 2019
#   Updated on 31 Oct 2019

from random import shuffle
from torch.utils.data import Dataset
import torch

class ExampleSet(Dataset):
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds a new empty ExampleSet object
    def __init__(self):
        self.examples = {}
        # self.examples[0] = []

    # Precond:
    #   example is a valid Example object.
    #
    # Postcond:
    #   Files the example away based on the agent ID in the example.
    #   If there is no agent ID in the example the example is filed under
    #   the 'default' key.
    def add_example(self, example):
        agent = example.get_agent()
        if agent is None:
            if 0 not in self.examples:
                self.examples[0] = []
            self.examples[0].append(example)
        else:
            if agent not in self.examples:
                self.examples[agent] = []
            self.examples[agent].append(example)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the agents who have examples in the example set.
    def get_agents(self):
        return self.examples.keys()

    # Precond:
    #   agent is the agent's dict key string.
    #
    # Postcond:
    #   Returns the number of examples from the agent.
    def agent_count(self, agent):
        return len(self.examples[agent])

    # Precond:
    #   example is a valid Example object.
    #
    # Postcond:
    #   Files the example away based on the agent ID in the example.
    #   If there is no agent ID in the example the example is filed under
    #   the 'default' key.
    def add_example_list(self, examples):
        for example in examples:
            agent = example.get_agent()
            if agent is None:
                self.examples[-1].append(example)
            else:
                if agent not in self.examples:
                    self.examples[agent] = []
                self.examples[agent].append(example)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a single list with all examples.
    def example_list(self):
        result = []
        for id,lst in self.examples.items():
            result.extend(lst)
        return result

    # Precond:
    #   None.
    #
    # Postcond:
    #   Shuffles the lists, internally, per agent ID
    def shuffle(self):
        for id in self.examples:
            shuffle(self.examples[id])

    # Precond:
    #   example is a valid Example object.
    #
    # Postcond:
    #   Turns an example into a structure which can be used for learning a neural
    #   network.
    def prepare_example(self, example):
        # label = torch.tensor(example.get_relation().neural_label())
        label = example.get_relation().value + 2
        pair = example.get_alts()
        inp = pair[0].values + pair[1].values
        inp = list(map(lambda x: float(x), inp))
        inp = torch.tensor(inp)
        label = torch.tensor(label)
        del pair
        return (inp,label)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through each examples (clumped by agent.)
    def each(self):
        for id,lst in self.examples.items():
            for ex in lst:
                yield ex

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through each flagged examples (clumped by agent.)
    def each_flagged(self):
        for id,lst in self.examples.items():
            for ex in lst:
                if ex.is_flagged():
                    yield ex

    # Precond:
    #   None.
    #
    # Postcond:
    #   Iterates through each unflagged examples (clumped by agent.)
    def each_unflagged(self):
        for id,lst in self.examples.items():
            for ex in lst:
                if not ex.is_flagged():
                    yield ex

    # Precond:
    #   None.
    #
    # Postcond:
    #   Unflags all examples.
    def unflag_all(self):
        for key in self.examples:
            for i in range(len(self.examples[key])):
                self.examples[key][i].unflag()

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the total number of examples in the set.
    def __len__(self):
        total = 0
        for id in self.examples:
            total += len(self.examples[id])
        return total

    # Precond:
    #   i is the index of the example ot retrieve.
    #
    # Postcond:
    #   Returns the ith example
    def __getitem__(self,i):
        for id in self.examples:
            if i >= len(self.examples[id]):
                i -= len(self.examples[id])
            else:
                return self.prepare_example(self.examples[id][i])
        return None

    # Precond:
    #   i is the index of the example ot retrieve.
    #
    # Postcond:
    #   Returns the ith example
    def get(self,i):
        for id in self.examples:
            if i >= len(self.examples[id]):
                i -= len(self.examples[id])
            else:
                return self.examples[id][i]
        return None

    # Precond:
    #   n is an integer representing the number of folds.
    #
    # Postcond:
    #   Returns an iterator which returns test and validation set.
    def crossvalidation(self,n):
        self.shuffle()
        for i in range(n):
            train = ExampleSet()
            valid = ExampleSet()
            count = 0
            # Before the validation slice
            for id in self.examples:
                # if len(self.examples[id]) <= 0:
                #     continue
                count = int(len(self.examples[id])/n)
                train.add_example_list(self.examples[id][0:count*i])
                # train.extend(self.examples[id][0:count*i])
            # The validation slice
            for id in self.examples:
                count = int(len(self.examples[id])/n)
                valid.add_example_list(self.examples[id][count*i:count+(count*i)])
                # valid.extend(self.examples[id][count*i:count+(count*i)])
            # After the validation slice
            for id in self.examples:
                count = int(len(self.examples[id])/n)
                train.add_example_list(self.examples[id][count+(count*i):])
                # train.extend(self.examples[id][count+(count*i):])
            # train = ExampleSet()
            # validation = ExampleSet()
            # train.add_example_list(temp_train)
            # validation.add_example_list(temp_valid)
            yield (train,valid)
            # del temp_train
            # del temp_valid
            del train
            del valid

    def __str__(self):
        ex = self.example_list()
        ex = list(map(lambda x: str(x),ex))
        return "\n".join(ex)

    # TODO: Parsing methods
