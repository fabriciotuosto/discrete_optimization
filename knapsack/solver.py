#!/usr/bin/python
# -*- coding: utf-8 -*-
from pulp import *
import sys, math
from collections import namedtuple, deque

Item = namedtuple("Item", ['index', 'value', 'weight'])

Node = namedtuple("Node", ['value', 'capacity', 'bound', 'item_index','taken'])

def constraint_programming_solve_it(items, capacity):
    knapsack = LpProblem('Knapsack', LpMaximize)
    xs = [LpVariable('x%s'%item.index, 0, 1, 'Binary') for item in items]
    knapsack += sum([x * item.value for x, item in zip(xs, items)]), 'obj'
    knapsack += sum([x * item.weight for x, item in zip(xs, items)]) <= capacity, 'c1'
    knapsack.solve()
    taken = [int(x.varValue) for x in xs]
    weight = sum([x * item.weight for x, item in zip(taken, items)])
    return value(knapsack.objective), weight, taken, knapsack.status


def simple_relaxation(items, capacity):
    return sum([item.value for item in items])

def linear_relaxation(items, capacity):
    remaining = capacity
    bound = 0
    for item in items:
        if remaining - item.weight >= 0:
            bound, remaining = bound + item.value, remaining - item.weight
        else:
            bound, remaining = bound + remaining * math.ceil(float(item.value) / item.weight), 0
            break

    return bound

def branch_bound_solve_it(items, capacity, bound_estimator):
    
    # items = sorted(items, key=lambda k: k.value, reverse=False)
    # items = sorted(items, key=lambda k: k.weight if not k.value else float(k.weight)/ k.value, reverse=True)
    items = sorted(items, key=lambda k: float(k.value)/float(k.weight), reverse=True)
    # items = sorted(items, key=lambda k: k.weight, reverse=False)
    best = root = Node(0, capacity, bound_estimator(items, capacity), 0, [])
    queue = deque()
    queue.append(root)
    while queue:
        
        node = queue.popleft()    
        # print 'Queue length:', len(queue), 'index:', node.item_index
        if node.item_index >= len(items) or node.bound < best.value: continue

        item  = items[node.item_index]

        left_bound = bound_estimator(items[node.item_index:], node.capacity)
        left  = Node(node.value + item.value, node.capacity - item.weight, left_bound, node.item_index + 1, node.taken + [item])
        
        right = Node(node.value, node.capacity, node.bound, node.item_index + 1, node.taken)
        
        if left.capacity > 0:
            best = left if left.value > best.value else best
            if left.bound > best.value:
                queue.append(left)

        if right.bound > best.value:
            queue.append(right)
        
    taken, weight = [0] * len(items), 0
    for item in best.taken:
        taken[item.index] = 1
        weight += item.weight
    return best.value, weight, taken

def dyna_solve_it(items, capacity):

    table = [[0 for w in range(capacity + 1)] for j in xrange(len(items) + 1)]
    for i, item in enumerate(items):
        j = i + 1
        for w in xrange(1, capacity + 1):
            table[j][w] = table[j-1][w] if w < item.weight else max(table[j-1][w], table[j-1][w] + item.weight)

    taken, value, weight, w = [0] * len(items), 0, 0, capacity
    for j in xrange(len(items), 0, -1):
        was_added = table[j][w] != table[j-1][w]
        taken[j-1] = 1 if was_added else 0
        if was_added:
            item = items[j-1]
            value, weight, w = value + item.value, weight + item.weight, w - item.weight

    return value, weight, taken

def greedy_solve_it(items, capacity):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return value, weight, taken

def parse_input(input_data, sorted=False):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    return capacity, items

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    capacity, items = parse_input(input_data)
    print 'Items:', len(items), 'capacity:', capacity
    value, weight, taken, optimal = constraint_programming_solve_it(items, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1 if optimal else 0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    
    if len(sys.argv) < 1:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
    else: 
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
        

