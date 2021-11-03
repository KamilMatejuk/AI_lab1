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

string Puzzle::short_state_repr() {

}

bool Puzzle::swap(Direction direction) {

}

void Puzzle::shuffle(int n) {

}

vector<Direction> Puzzle::get_possible_moves() {

}

bool Puzzle::is_finished() {

}

void Puzzle::show() {

}
