#include "puzzle.h"
#include "heuristic.h"
#include <iostream>
#include <cmath>
#include <math.h>


int heuristic1(Puzzle puzzle) {
    int distances = 0;
    int expected_x;
    int expected_y;

    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            if(puzzle.positions[i][j]==0) {
                puzzle.positions[i][j] = pow(Puzzle::SIZE, 2);
            }
            expected_x = (puzzle.positions[i][j] - 1) % Puzzle::SIZE;
            expected_y = floor((puzzle.positions[i][j]-1)/Puzzle::SIZE);
            distances += abs(j - expected_x) + abs(i - expected_y);
        }
    }
    return Puzzle::SIZE * distances;
}

int heuristic2(Puzzle puzzle) {
    int incorrect = 0;
    int expected_x;
    int expected_y;

    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            if(puzzle.positions[i][j]==0) {
                puzzle.positions[i][j] = pow(Puzzle::SIZE, 2);
            }
            expected_x = (puzzle.positions[i][j] - 1) % Puzzle::SIZE;
            expected_y = floor((puzzle.positions[i][j]-1)/Puzzle::SIZE);
            if((i != expected_y) || (j != expected_x)) {
                incorrect += 1;
            }
        }
    }
    return Puzzle::SIZE * incorrect;
}
