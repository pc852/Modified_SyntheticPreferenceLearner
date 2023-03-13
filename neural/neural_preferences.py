# File: neural_preferences.py
# Author: Michael Huelsman
# Created On: 18 March 2020
# Purpose:
#   A neural net for learning preferences directly from examples.

import torch
import torch.nn as nn
# import torch.nn.function as F
import torch.optim as optim
from torch.utils.data import DataLoader

class NeuralPreference(nn.Module):
    def __init__(self, size, domain):
        super(NeuralPreference, self).__init__()
        size.insert(0,domain.length()*2)
        size.append(6)
        self.layers = [nn.Linear(size[i],size[i+1]) for i in range(len(size)-1)]
        self.layers = nn.ModuleList(self.layers)
        self.internal = nn.ReLU()
        self.squash = nn.LogSoftmax(dim=0)

    def forward(self, x):
        for i in range(len(self.layers)):
            if i != 0:
                x = self.internal(x)
            x = self.layers[i](x)
        # x = self.squash(x)
        return x

    def forward_squash(self, x):
        for i in range(len(self.layers)):
            if i != 0:
                x = self.internal(x)
            x = self.layers[i](x)
        x = self.squash(x)
        return x


# Precond:
#   example is a valid Example object.
#
# Postcond:
#   Turns an example into a structure which can be used for learning a neural
#   network.
def prepare_example(example):
    # label = torch.tensor(example.get_relation().neural_label())
    label = example.get_relation().value + 2
    pair = example.get_alts()
    inp = pair[0].values + pair[1].values
    inp = list(map(lambda x: float(x), inp))
    inp = torch.tensor(inp)
    return (inp,label)


# Precond:
#   ex_set is a valid ExampleSet object.
#   layers is a list of integers indicating the layer sizes.
#   epochs is an integer indicating the number of epochs to train for.
#   domain is a valid Domain object.
#   device is the device where the learner should reside.
#
# Postcond:
#   Trains and returns a neural net which has learned off the given example set.
def train_neural_preferences(ex_set, layers, epochs, domain, device=None):
    result = NeuralPreference(layers, domain)
    if device is not None:
        result = result.to(device)
    # criterion = nn.L1Loss()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(result.parameters(), lr=0.01)
    # scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=2)
    scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=100)
    for epoch in range(epochs):
        globalLoss = 0.0
        for examples in DataLoader(dataset=ex_set, batch_size=10, pin_memory=True):
            inps = labels = None
            if device is not None:
                inps, labels = examples[0].to(device), examples[1].to(device)
            else:
                inps, labels = examples
            optimizer.zero_grad()
            outputs = result(inps)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            globalLoss += loss.item()
            del inps
            del loss
            del labels
            del outputs
            del examples
        scheduler.step(globalLoss)
        # print(epoch,"->",globalLoss)
    del ex_set
    del optimizer
    # del scheduler
    del criterion
    return result

# Precond:
#   ex_set is a valid ExampleSet object.
#   layers is a list of integers indicating the layer sizes.
#   epochs is an integer indicating the number of epochs to train for.
#   domain is a valid Domain object.
#   device is the device where the learner should reside.
#
# Postcond:
#   Trains and returns a neural net which has learned off the given example set.
def train_neural_preferences_curve(ex_set, layers, epochs, domain, device=None):
    result = NeuralPreference(layers, domain)
    samples = []
    if device is not None:
        result = result.to(device)
    # criterion = nn.L1Loss()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(result.parameters(), lr=0.01)
    # scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=2)
    scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=100)
    for epoch in range(epochs):
        globalLoss = 0.0
        for examples in DataLoader(dataset=ex_set, batch_size=10, pin_memory=True):
            inps = labels = None
            if device is not None:
                inps, labels = examples[0].to(device), examples[1].to(device)
            else:
                inps, labels = examples
            optimizer.zero_grad()
            outputs = result(inps)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            globalLoss += loss.item()
            del inps
            del loss
            del labels
            del outputs
            del examples
        scheduler.step(globalLoss)
        if(epoch%10 == 0 or epoch == epochs-1):
            samples.append(globalLoss)
        # print(epoch,"->",globalLoss)
    del ex_set
    del optimizer
    # del scheduler
    del criterion
    return (result,samples)
