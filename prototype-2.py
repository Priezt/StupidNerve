#!/usr/bin/env python

import random
import math

class Brain:
    POUR_RATE = 0.01
    PICK_RATE = 0.2
    GENERATE_PROBABILITY = 0.01
    SURVIVE_RATE = 0.5

    def __init__(self):
        self.ns = set()

    def add(self, n):
        self.ns.add(n)

    def show(self):
        for n in self.ns:
            print n.dump()

    def think(self):
        self.reset()
        self.spread()
        self.survive()
        self.clear()
        self.pick()
        self.pour()
        self.reborn()
        self.input()
        self.output()
        self.rebind()
        self.generate()

    def input(self):
        """
            Sense to out-world
        """
        pass

    def output(self):
        """
            Do action
        """
        pass

    def generate(self):
        """
            If two neurons are activated at the same time,
            have a chance to generate a new neuron
            connected to both of these neurons
        """
        ns = filter(lambda x: x.activated, list(self.ns))
        for x in range(len(ns)-1):
            for y in range(x + 1, len(ns)):
                if random.random <= Brain.GENERATE_PROBABILITY:
                    n = Neuron()
                    self.add(n)
                    ns[x].connect(n)
                    ns[y].connect(n)

    def survive(self):
        """
            Mark neurons to survive
        """
        ns = filter(lambda x: x.activated, list(self.ns))
        for n in ns:
            if random.random() < Brain.SURVIVE_RATE:
                n.survive = True

    def reborn(self):
        """
            Make neurons to reborn
        """
        for n in self.ns:
            if n.survive:
                n.activate()
                n.survive = False

    def rebind(self):
        """
            If two neurons are activated at the same time,
            connect them or add link power
        """
        ns = filter(lambda x: x.activated, list(self.ns))
        for x in range(len(ns)-1):
            for y in range(x + 1, len(ns)):
                if ns[x].connected(ns[y]):
                    ns[x].get_link(ns[y]).grow()
                else:
                    ns[x].connect(ns[y])

    def pick(self):
        """
            Pick neurons with highest power value
            and activate them
        """
        count = self.get_count(Brain.PICK_RATE)
        sorted_ns = sorted(self.ns, cmp=lambda x,y: cmp(y.power, x.power))
        for n in sorted_ns[:count]:
            n.activate()

    def spread(self):
        """
            Add power to neurons which are connected to
            currently activated neurons
        """
        for n in self.ns:
            if n.activated:
                for l in n.ls:
                    n_a = l.neighbour(n)
                    n_a.power += random.random() * math.log(l.v)

    def reset(self):
        """
            Set power of all neurons to 0
        """
        for n in self.ns:
            n.power = 0

    def clear(self):
        """
            Inactivate all neurons
        """
        for n in self.ns:
            n.clear()

    def get_count(self, rate):
        return max(1, int(len(self.ns) * rate))

    def pour(self):
        """
            Activate several neurons randomly
        """
        ns = list(self.ns)
        count = self.get_count(Brain.POUR_RATE)
        length = len(ns)
        for i in range(count):
            idx  = random.randint(i, length - 1)
            t = ns[i]
            ns[i] = ns[idx]
            ns[idx] = t
            ns[i].activate()

class Neuron:
    INCREMENT_ID = 0

    def get_id(self):
        Neuron.INCREMENT_ID += 1
        self.id = Neuron.INCREMENT_ID
        return self.id

    def __init__(self):
        self.ls = set()
        self.get_id()
        self.activated = False
        self.power = 0
        self.survive = False

    def activate(self):
        self.activated = True

    def clear(self):
        self.activated = False

    def __str__(self):
        return "N%s" % self.id

    def flag(self):
        if self.activated:
            return "*"
        else:
            return " "

    def dump(self):
        return "%s%s : %s" % (self, self.flag(), " ".join([l.dump(self) for l in self.ls]))

    def connect(self, n):
        if not self.connected(n):
            l = Link(self, n)
            self.ls.add(l)
            n.ls.add(l)

    def disconnect(self, n):
        if self.connected(n):
            self.get_link(n).destroy()

    def get_link(self, n):
        if self.connected(n):
            for l in self.ls:
                if n in l.nodes:
                    return l

    def connected(self, n):
        for l in self.ls:
            if n in l.nodes:
                return True
        return False

class Link:
    MAX_V = 1000

    def __init__(self, n1, n2):
        self.nodes = set()
        self.nodes.add(n1)
        self.nodes.add(n2)
        self.v = 1

    def grow(self):
        self.v += 1
        if self.v > Link.MAX_V:
            self.v = Link.MAX_V

    def destroy(self):
        for n in self.nodes:
            n.ls.remove(self)

    def dump(self, n):
        for i in self.nodes:
            if i != n:
                return "%s(%s)" % (i, self.v)

    def neighbour(self ,n):
        for i in self.nodes:
            if i != n:
                return i

if __name__ == "__main__":
    bn = Brain()
    for i in range(12):
        bn.add(Neuron())
    for i in range(1000):
        bn.think()
    bn.show()

