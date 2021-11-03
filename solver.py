import sys
import copy
import time
from puzzle import Puzzle, DIRECTIONS
from typing import Callable, List

class Solver():
    def __init__(self, puzzle: Puzzle, heuristic: Callable):
        # self.puzzle = puzzle
        self.heuristic = heuristic
        self.visited_states: List[Puzzle] = []
        self.states_to_visit: List[Puzzle] = [puzzle]
        self.solution: Puzzle = None
        self.solving_time = 0
    
    def solve(self):
        self.start_time = time.time()
        while len(self.states_to_visit) != 0:
            # find node with least f
            min_f = sys.maxsize
            min_state = None
            for state in self.states_to_visit:
                h = self.heuristic(state)
                g = len(state.solution_path)
                f = g + h
                if f < min_f:
                    min_f = f
                    min_state = state
            assert min_state is not None
            print(f'Found minimal state: {min_state.short_state_repr()} -> f = g + h = {min_f}')
            del min_f, state
            # pop off list
            self.states_to_visit.remove(min_state)
            # for each successor:
            next_moves = min_state.get_possible_moves()
            for move in next_moves:
                print(f'Checking successor after move {move}')
                succ = copy.deepcopy(min_state)
                succ.puzzle_swap(move)
                # check if finished
                if succ.is_finished():
                    self.solution = succ
                    self.solving_time = time.time() - self.start_time
                    print(f'Found final solution in {self.solving_time}: ({len(succ.solution_path)}) {succ.solution_path}')
                    return
                # f = g + h
                succ_f  = len(succ.solution_path)  + self.heuristic(succ)
                print(f'After move f = {succ_f}')
                
                # check if already in list to visit with lower value
                already_exists_with_lower_f = False
                for state in self.states_to_visit:
                    if state.short_state_repr() == succ.short_state_repr():
                        state_f = len(state.solution_path) + self.heuristic(state) # f = g + h
                        if state_f < succ_f:
                            already_exists_with_lower_f = True
                            break
                print(f'Checking if already exists with lower f in open list -> {already_exists_with_lower_f}')
                if already_exists_with_lower_f:
                    continue
                # check if already visited with lower value
                already_exists_with_lower_f = False
                for state in self.visited_states:
                    if state.short_state_repr() == succ.short_state_repr():
                        state_f = len(state.solution_path) + self.heuristic(state) # f = g + h
                        if state_f < succ_f:
                            already_exists_with_lower_f = True
                            break
                print(f'Checking if already exists with lower f in closed list -> {already_exists_with_lower_f}')
                if already_exists_with_lower_f:
                    continue
                # otherwise add to list
                self.states_to_visit.append(succ)
                print(f'Added {succ.short_state_repr()} to the open list')
            self.visited_states.append(min_state)
            del move, min_state, already_exists_with_lower_f
            
    def get_data(self):
        if self.solution is None:
            return {
                'number of visited states': len(self.visited_states),
            }
        else:
            return {
                'number of visited states': len(self.visited_states),
                'path length': len(self.solution.solution_path),
                'path': self.solution.solution_path,
                'time': self.solving_time
            }
    
    @classmethod
    def compare(cls, datadict: dict):
        avg = lambda l: 'no data' if len(l) == 0 else sum(l) / len(l)
        for key in datadict:
            data = datadict[key]
            print(f'{key} ({len(data)} items): time {avg([float(i.get("time")) for i in data])} {[float(i.get("time")) for i in data]}')
        for key in datadict:
            print(f'{key} {datadict[key]}')
