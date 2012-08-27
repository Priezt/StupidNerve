#!/usr/bin/env python

class Brain:
    def __init__(self):
        self.neurons = []

    def add(self, n):
        self.neurons.append(n)
        n.uid = len(self.neurons) - 1
        n.container = self
    
    def tick(self):
        pass

class Neuron:
    pass

if __name__ == '__main__':
    bn = Brain()
    n = Neuron()
    bn.add(n)
    print bn
    print n
