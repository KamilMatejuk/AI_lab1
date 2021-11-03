#include "puzzle.h"
#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
using namespace std;


string get_direction_name(Direction d) {
    string name = "";
    switch (d) {
        case Direction::DOWN:  name = "DOWN";  break;
        case Direction::RIGHT: name = "RIGHT"; break;
        case Direction::UP:    name = "UP";    break;
        case Direction::LEFT:  name = "LEFT";  break;
    }
    return name;
}

Puzzle::Puzzle() {
    // create starting positions
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            positions[i][j] = SIZE * i + j + 1;
        }
    }
    empty_x = SIZE - 1;
    empty_y = SIZE - 1;
    positions[empty_y][empty_x] = 0;
    cout << short_state_repr() << endl;
    // shuffle
    shuffle(pow(SIZE, 4));
    solution_path = {};
};

Puzzle::Puzzle(bool _shuffle) {
    // create starting positions
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            positions[i][j] = SIZE * i + j + 1;
        }
    }
    empty_x = SIZE - 1;
    empty_y = SIZE - 1;
    positions[empty_y][empty_x] = 0;
    cout << short_state_repr() << endl;
    // shuffle
    if (_shuffle) {
        shuffle(pow(SIZE, 4));
    }
    solution_path = {};
};

Puzzle Puzzle::copy() {
    Puzzle p = Puzzle(false);
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            p.positions[i][j] = positions[i][j];
        }
    }
    p.empty_x = empty_x;
    p.empty_y = empty_y;
    for (Direction d : solution_path) {
        p.solution_path.push_back(d);
    }
    return p;
}

string Puzzle::short_state_repr() {
    string repr = "";
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            repr += to_string(positions[i][j]) + "|";
        }
    }
    return repr.substr(0, repr.size() - 1);
}

bool Puzzle::swap(Direction direction) {
    float angle_radians = (PI * direction / 180);
    int x = round(empty_x + sin(angle_radians));
    int y = round(empty_y - cos(angle_radians));
    // check if in range
    if (x < 0 || x >= SIZE || y < 0 || y >= SIZE) {
        return false;
    }
    // check if adjacent
    if (!(x == empty_x && abs(y - empty_y) == 1) && \
        !(y == empty_y && abs(x - empty_x) == 1)) {
        return false;
    }
    // swap
    positions[empty_y][empty_x] = positions[y][x];
    positions[y][x] = 0;
    cout << "Swapped (" + to_string(empty_x) + ", " + to_string(empty_y) + ") " +\
            get_direction_name(direction) + " to (" + to_string(x) + ", " + to_string(y) +\
             ")" << endl;
    empty_x = x;
    empty_y = y;
    solution_path.push_back(direction);
    return true;
}

void Puzzle::shuffle(int n) {
    int i = 0;
    Direction last_direction = Direction::LEFT;
    while (i < n) {
        vector<Direction> possible_dirs = get_possible_moves();
        Direction d = possible_dirs[rand() % possible_dirs.size()];
        // opposite to last direction
        if (abs(d - last_direction) == 180) {
            continue;
        }
        // swap
        if (swap(d)) {
            last_direction = d;
            i++;
        }
    }
    // return empty place to lower right corner
    for (int i = empty_x; i < SIZE - 1; i++) {
        swap(Direction::RIGHT);
    }
    for (int i = empty_y; i < SIZE - 1; i++) {
        swap(Direction::DOWN);
    }
}

vector<Direction> Puzzle::get_possible_moves() {
    Direction dirs[4] = { UP, RIGHT, DOWN, LEFT };
    vector<Direction> possible_dirs;
    for (int i = 0; i < 4; i++) {
        Direction d = dirs[i];
        float angle_radians = (PI * d / 180);
        int x = round(empty_x + sin(angle_radians));
        int y = round(empty_y - cos(angle_radians));
        // check if in range
        if (x >= 0 && x < SIZE && y >= 0 && y < SIZE) {
            possible_dirs.push_back(d);
        }
    }
    return possible_dirs;
}

bool Puzzle::is_finished() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int p = positions[i][j];
            if (p == 0) {
                p = SIZE * SIZE;
            }
            int expected_x = (p - 1) % SIZE;
            int expected_y = int((p - 1) / SIZE);
            if (expected_y != i || expected_x != j) {
                return false;
            }
        }
    }
    return true;
}

void Puzzle::show() {
    string edge = "+";
    for (int i = 0; i < SIZE; i++) {
        edge += "----+";
    }
    cout << endl;
    cout << edge << endl;
    for (int i = 0; i < SIZE; i++) {
        cout << "|";
        for (int j = 0; j < SIZE; j++) {
            int p = positions[i][j];
            if (p == 0) {
                cout << "    |";
            } else if (p > 9) {
                cout << " " << positions[i][j] << " |";
            } else {
                cout << "  " << positions[i][j] << " |";
            }
        }
        cout << endl;
        cout << edge << endl;
    }
}
