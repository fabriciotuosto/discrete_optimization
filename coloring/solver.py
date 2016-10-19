#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from pulp import *

def constraint_programming_solve_it(edges):
    adjacents = defaultdict(list)
    graph_coloring = LpProblem('Graph Coloring', LpMinimize)
    nodes = { node for node, _ in edges }.union({node for _, node in edges})
    nodes = sorted(list(nodes))
    xs = { x: LpVariable('x%s'%x, 0, len(nodes), 'Integer') for x in nodes}
    for x,y in edges:
        adjacents[xs[x]].append(xs[y])

    graph_coloring += lpSum(xs.values()), 'objective'
    for x, adj in adjacents.iteritems():
        for y in adj:
            graph_coloring += y - x >= 1, 'x :%s distinct adj :%s'%(x,y)
    graph_coloring.solve()
    colors = [int(x.varValue) for x in xs.values()]
    print 'Colors', len(set(colors))
    return colors

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    solution = constraint_programming_solve_it(edges)

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

