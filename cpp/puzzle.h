#pragma once
#include <string>
#include <vector>
using namespace std;

static const float PI = 3.14159;

enum Direction {
    // angle from vertical
    UP    = 0,
    RIGHT = 90,
    DOWN  = 180,
    LEFT  = 270
};

string get_direction_name(Direction d);

class Puzzle {
    public:
        static const int SIZE = 4;
        int positions[SIZE][SIZE];
        vector<Direction> solution_path;
        int empty_x;
        int empty_y;

        friend bool operator== (const Puzzle &p1, const Puzzle &p2);
        
        Puzzle();
        Puzzle(bool _shuffle);
        Puzzle copy();
        string short_state_repr();
        bool swap(Direction direction);
        void shuffle(int n);
        vector<Direction> get_possible_moves();
        bool is_finished();
        void show();
};
