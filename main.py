# from __future__ import print_function
# from sys import getsizeof, stderr
# from itertools import chain
# from collections import deque
# try:
#     from reprlib import repr
# except ImportError:
#     pass

import sys
import copy
import tracemalloc
from puzzle import Puzzle, DIRECTIONS
from solver import Solver
from utils import section_name, iteration_name

def heuristic1(puzzle: Puzzle):
    # distance to target for each cell
    distances = 0
    for current_y, row in enumerate(puzzle.positions):
        for current_x, p in enumerate(row):
            if p == 0:
                p = Puzzle.SIZE ** 2
            expected_x = (p - 1) % Puzzle.SIZE
            expected_y = int((p - 1) / Puzzle.SIZE)
            distances += abs(current_x - expected_x) + abs(current_y - expected_y)
    
    
    return Puzzle.SIZE * distances

# def heuristic2(puzzle: Puzzle):
#     # number of cells in incorrect position
#     incorrect = 0
#     for current_y, row in enumerate(puzzle.positions):
#         for current_x, p in enumerate(row):
#             if p == 0:
#                 p = Puzzle.SIZE ** 2
#             expected_x = (p - 1) % Puzzle.SIZE
#             expected_y = int((p - 1) / Puzzle.SIZE)
#             if (current_y != expected_y) or (current_x != expected_x):
#                 incorrect += 1
#     return Puzzle.SIZE * incorrect
            


# def total_size(o, handlers={}, verbose=False):
#     """ Returns the approximate memory footprint an object and all of its contents.

#     Automatically finds the contents of the following builtin containers and
#     their subclasses:  tuple, list, deque, dict, set and frozenset.
#     To search other containers, add handlers to iterate over their contents:

#         handlers = {SomeContainerClass: iter,
#                     OtherContainerClass: OtherContainerClass.get_elements}

#     """
#     dict_handler = lambda d: chain.from_iterable(d.items())
#     all_handlers = {tuple: iter,
#                     list: iter,
#                     deque: iter,
#                     dict: dict_handler,
#                     set: iter,
#                     frozenset: iter,
#                    }
#     all_handlers.update(handlers)     # user handlers take precedence
#     seen = set()                      # track which object id's have already been seen
#     default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

#     def sizeof(o):
#         if id(o) in seen:       # do not double count the same object
#             return 0
#         seen.add(id(o))
#         s = getsizeof(o, default_size)

#         if verbose:
#             print(s, type(o), repr(o), file=stderr)

#         for typ, handler in all_handlers.items():
#             if isinstance(o, typ):
#                 s += sum(map(sizeof, handler(o)))
#                 break
#         return s

#     return sizeof(o)

if __name__ == "__main__":
    tracemalloc.start()
    heuristics = [heuristic1] #, heuristic2]
    solving_data = { h.__name__: [] for h in heuristics }
    
        
    # tracemalloc.start()
    # dir_list_names = [Puzzle() for _ in range(10**5)]
    # print(f'size of object in bytes 1: {sys.getsizeof(dir_list_names)}')
    # print(f'size of object in bytes 2: {total_size(dir_list_names)}')
    # print(f'Peak memory usage: {tracemalloc.get_traced_memory()} memory blocks')
    # exit()
    
    for j in range(1):
        try:
            print(iteration_name(f'Running test {j + 1}'))
            print(section_name('Generating random 15 Puzzle'))
            # random starting permutation
            puzzle = Puzzle()
            puzzle.show()
            # solve with heuristics
            for i, heuristic in enumerate(heuristics):
                print(section_name(f'Solving with heuristic {i + 1}'))
                s = Solver(copy.deepcopy(puzzle), heuristic)
                s.solve()
                solving_data[heuristic.__name__].append(s.get_data())
                # break
                del s
            del puzzle
        except:
            continue

    # compare results
    print(iteration_name('Compare results'))
    print(f'Peak memory usage: {tracemalloc.get_traced_memory()[1]} memory blocks')
    Solver.compare(solving_data)
