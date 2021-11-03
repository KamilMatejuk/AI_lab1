#include "puzzle.h"
#include <iostream>
#include <string>

Puzzle::Puzzle() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            positions[i][j] = SIZE * i + j + 1;
        }
    }
};
