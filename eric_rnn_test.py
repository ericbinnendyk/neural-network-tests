# a test where I try to create a Random Neural Network similar to what is described here: http://www.irisa.fr/armor/lesmembres/Rubino/Publis2005/RNN.pdf

import sched, time

from random import random

s = sched.scheduler(time.time, time.sleep)

# random real from 0 to x
def rand(x):
    return random() * x

class Node():
    def __init__(self, name, freq, positive_prob):
        self.potential = 1
        self.name = name
        self.freq = freq
        self.pos_prob = positive_prob
        self.neighbors = []
    def connect(self, neighbor):
        self.neighbors.append(neighbor)
        neighbor.neighbors.append(self)
    def increase_potential(self):
        self.potential += 1
    def decrease_potential(self):
        if self.potential > 0:
            self.potential -= 1
    def __str__(self):
        return "Neuron {}\n\tPotential: {}\n\tFreq: {}\n\tPositive probability: {}\n\tNeighbors: {}\n".format(self.name, self.potential, self.freq, self.pos_prob, [neigh.name for neigh in self.neighbors])

# sends out a random signal to a random neighbor
def send_signal(node):
    if len(node.neighbors) == 0:
        print("Error: No neighbors on node.")
        exit()
    if node.potential > 0:
        node.potential -= 1
        for neigh in node.neighbors:
            x = rand(1)
            if x < node.pos_prob:
                neigh.increase_potential()
            else:
                neigh.decrease_potential()
    r = rand(node.freq)
    s.enter(r, 1, send_signal, argument=(node, ))

# print node status every 2 seconds
def print_status(node_list):
    for node in node_list:
        print(node)
    s.enter(2, 1, print_status, argument = (node_list, ))

# initialize nodes
n1 = Node("Node1", 0.5, 0.85)
n2 = Node("Node2", 0.3, 0.9)
n3 = Node("Node3", 1.5, 0.6)
n4 = Node("Node4", 1.0, 0.8)
n5 = Node("Node5", 0.9, 0.75)
nodes = [n1, n2, n3, n4, n5]

# connect nodes
n1.connect(n2)
n2.connect(n3)
n3.connect(n4)
n4.connect(n5)
n5.connect(n1)

s.enter(0, 1, print_status, argument = (nodes, ))
s.enter(0.1, 1, send_signal, argument = (n1, ))
s.enter(0.2, 1, send_signal, argument = (n2, ))
s.enter(0.3, 1, send_signal, argument = (n3, ))
s.enter(0.4, 1, send_signal, argument = (n4, ))
s.enter(0.5, 1, send_signal, argument = (n5, ))

s.run()