import random
from enum import Enum
from utils import center


class Direction(Enum):
    LEFT  = [-1,  0]
    RIGHT = [ 1,  0]
    UP    = [ 0, -1]
    DOWN  = [ 0,  1]
    
    @classmethod
    def reverse(cls, dir):
        if dir == Direction.LEFT:  return Direction.RIGHT
        if dir == Direction.RIGHT: return Direction.LEFT
        if dir == Direction.UP:    return Direction.DOWN
        if dir == Direction.DOWN:  return Direction.UP

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


class Puzzle:
    SIZE = 4
    def __init__(self):
        self.solution_path = []
        # create starting positions
        self.positions = [[self.SIZE * i + j + 1 for j in range(self.SIZE)] for i in range(self.SIZE)]
        # empty field in lower right corner
        self.empty_x = self.SIZE - 1
        self.empty_y = self.SIZE - 1
        self.positions[self.empty_y][self.empty_x] = 0
        # shuffle
        self.shuffle_path = []
        self.shuffle(self.SIZE ** 4)
        self.shuffle_path = []
        self.solution_path = []
    
    def short_state_repr(self) -> str:
        """ Represent currect state as short string """
        return '|'.join('|'.join(str(p) for p in row) for row in self.positions)

    def puzzle_swap(self, dir: Direction) -> bool:
        """ Execute swap according to game rules (only swap adjacent to empty)

        Args:
            dir (Direction): in what direction move empty cell

        Returns:
            bool: was the swap successfull?
        """
        dir_x = dir.value[0]
        dir_y = dir.value[1]
        successfull = self.swap(self.empty_x, 
                                self.empty_y,
                                self.empty_x + dir_x,
                                self.empty_y + dir_y)
        if successfull:
            self.empty_x += dir_x
            self.empty_y += dir_y
            self.solution_path.append(dir)
        return successfull

    def swap(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """ Swap two adjacent cells

        Args:
            x1 (int): column of first cell
            y1 (int): row of first cell
            x2 (int): column of second cell
            y2 (int): row of second cell

        Returns:
            bool: was the swap successfull?
        """
        try:
            # check values
            assert 0 <= x1 < self.SIZE
            assert 0 <= y1 < self.SIZE
            assert 0 <= x2 < self.SIZE
            assert 0 <= y2 < self.SIZE
            # check if positions are adjacent
            if ((x1 == x2 and abs(y1 - y2) == 1) or 
                (y1 == y2 and abs(x1 - x2) == 1)):
                # check if one is free
                if ((self.positions[y1][x1] == 0) or
                    (self.positions[y2][x2] == 0)):
                    # swap
                    temp = self.positions[y1][x1]
                    self.positions[y1][x1] = self.positions[y2][x2]
                    self.positions[y2][x2] = temp
                    return True
        except (IndexError, AssertionError):
            pass
        return False

    def shuffle(self, n: int):
        """ Run multiple random swaps to shuffle puzzle,
        and return empty cell to lower right corner

        Args:
            n (int): number of swaps
        """
        self.shuffle_path = []
        # randomize positions
        i = 0
        last_direction = Direction.LEFT.value
        while i < n:
            d = random.choice(self.get_possible_moves())
            if d.value[0] == -last_direction[0] and d.value[1] == -last_direction[1]:
                continue
            if self.puzzle_swap(d):
                self.shuffle_path.append(d)
                last_direction = d.value
                i += 1
        # return empty place to lower right corner
        for _ in range(self.empty_x, self.SIZE - 1):
            d = Direction.RIGHT
            if self.puzzle_swap(d):
                self.shuffle_path.append(d)
        for _ in range(self.empty_y, self.SIZE - 1):
            d = Direction.DOWN
            if self.puzzle_swap(d):
                self.shuffle_path.append(d)
        # show path
        print(f'Path taken to shuffle ({len(self.shuffle_path)} steps):')
        print(' -> '.join(p.name for p in self.shuffle_path))

    def reverse_shuffle(self):
        for p in self.shuffle_path[::-1]:
            self.puzzle_swap(Direction.reverse(p))

    def get_possible_moves(self):
        dirs = []
        for d in DIRECTIONS:
            if (0 <= self.empty_x + d.value[0] < self.SIZE) and \
                (0 <= self.empty_y + d.value[1] < self.SIZE):
                dirs.append(d)
        return dirs

    def is_finished(self):
        correct_positions = [[self.SIZE * i + j + 1 for j in range(self.SIZE)] for i in range(self.SIZE)]
        correct_positions[self.SIZE - 1][self.SIZE - 1] = 0
        correct_short = '|'.join('|'.join(str(p) for p in row) for row in correct_positions)
        return self.short_state_repr() == correct_short

    def show(self):
        """ Display puzzle on stdout """
        edge = '+' + '+'.join('----' for _ in range(self.SIZE)) + '+'
        print()
        print(center(edge))
        for row in self.positions:
            row_temp = []
            for p in row:
                if p != 0: row_temp.append(f' {p:#2} ')
                else:      row_temp.append(f'    ')
            print(center('|' + '|'.join(p for p in row_temp) + '|'))
            print(center(edge))
        print()
