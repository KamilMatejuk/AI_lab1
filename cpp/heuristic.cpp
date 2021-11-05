#include "puzzle.h"
#include "heuristic.h"
#include <iostream>
#include <cmath>
#include <math.h>


int heuristic1(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position
    // with weights depending on cell nr
    // (1 is most important, 15 is least important)
    // summed with exponential distance from empty space to first not ordered cell
    int distances = 0;
    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            int expected_x = (p - 1) % Puzzle::SIZE;
            int expected_y = floor((p - 1) / Puzzle::SIZE);
            int d = abs(j - expected_x) + abs(i - expected_y);
            int importance = pow(Puzzle::SIZE, 2) - p;
            distances += d * importance;
        }
    }
    // distance from empty to first not ordered
    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            int expected_x = (p - 1) % Puzzle::SIZE;
            int expected_y = floor((p - 1) / Puzzle::SIZE);
            if((i != expected_y) || (j != expected_x)) {
                int d = abs(j - puzzle.empty_x) + abs(i - puzzle.empty_y);
                int importance = pow(Puzzle::SIZE, 2) - p;
                distances += d * importance * importance;
                goto endloop;
            }
        }
    }
    endloop:
    return Puzzle::SIZE * distances;
}

int heuristic2(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position
    // with weights depending on cell nr
    // (1 is most important, 15 is least important)
    int distances = 0;
    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            int expected_x = (p - 1) % Puzzle::SIZE;
            int expected_y = floor((p - 1) / Puzzle::SIZE);
            int d = abs(j - expected_x) + abs(i - expected_y);
            int importance = pow(Puzzle::SIZE, 2) - p;
            distances += d * importance;
        }
    }
    return Puzzle::SIZE * distances;
}

int heuristic3(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position 
    int distances = 0;
    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            int expected_x = (p - 1) % Puzzle::SIZE;
            int expected_y = floor((p - 1) / Puzzle::SIZE);
            distances += abs(j - expected_x) + abs(i - expected_y);
        }
    }
    return Puzzle::SIZE * distances;
}