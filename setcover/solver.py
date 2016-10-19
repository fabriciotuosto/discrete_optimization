#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pulp import *
from collections import namedtuple, OrderedDict
from itertools import izip
Set = namedtuple("Set", ['index', 'cost', 'items'])

def constraint_programming_solve_it(cover_sets):
    def coverage_constraint_item(item):
        return lpSum([1 * x for i, x in enumerate(xs) if item in cover_sets[i].items]) >= 1

    items = {item for s in cover_sets for item in s.items}
    set_cover = LpProblem('Set Cover', LpMinimize)
    xs = [LpVariable('x%s'%cover_set.index, 0, 1, 'Binary') for cover_set in cover_sets]
    costs = [x.cost for x in cover_sets]
    set_cover += lpSum([x * cost for x, cost in izip(xs, costs)]), 'objective'
    set_cover.constraints = OrderedDict([('covered_'+str(item), coverage_constraint_item(item)) for item in items])
    print set_cover
    set_cover.solve(GLPK(msg=0))
    taken = [int(x.varValue) for x in xs]
    return value(set_cover.objective), taken, set_cover.status

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    print 'Sets', set_count, 'items', item_count
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), map(int, parts[1:])))

    # build a trivial solution
    # pick add sets one-by-one until all the items are covered
    objective, solution, optimal = constraint_programming_solve_it(sets)

    # prepare the solution in the specified output format
    output_data = str(objective) + ' ' + str(1 if optimal else 0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

