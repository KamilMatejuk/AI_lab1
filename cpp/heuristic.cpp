#include "puzzle.h"
#include "heuristic.h"
#include <iostream>
#include <cmath>
#include <math.h>


int heuristic1(Puzzle& puzzle) {
    int incorrect = 0;
    int expected_x;
    int expected_y;

    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            expected_x = (p - 1) % Puzzle::SIZE;
            expected_y = floor((p - 1) / Puzzle::SIZE);
            if((i != expected_y) || (j != expected_x)) {
                incorrect += 1;
            }
        }
    }
    return Puzzle::SIZE * incorrect;
}

int heuristic2(Puzzle& puzzle) {
    int distances = 0;
    int expected_x;
    int expected_y;

    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            expected_x = (p - 1) % Puzzle::SIZE;
            expected_y = floor((p - 1) / Puzzle::SIZE);
            distances += abs(j - expected_x) + abs(i - expected_y);
        }
    }
    return Puzzle::SIZE * distances;
}

int heuristic3(Puzzle& puzzle) {
    int distances = 0;
    int expected_x;
    int expected_y;

    for (int i = 0; i < Puzzle::SIZE; i++) {
        for (int j = 0; j < Puzzle::SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(Puzzle::SIZE, 2);
            }
            expected_x = (p - 1) % Puzzle::SIZE;
            expected_y = floor((p - 1) / Puzzle::SIZE);
            int d = abs(j - expected_x) + abs(i - expected_y);
            int importance = pow(Puzzle::SIZE, 2) - p;
            distances += d * importance;
        }
    }
    return Puzzle::SIZE * distances;
}
