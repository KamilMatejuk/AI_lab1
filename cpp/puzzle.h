#include <string>
using namespace std;


class Direction {
    public:
        const int LEFT[2]  = {-1,  0};
        const int RIGHT[2] = {1, 0};
        const int UP[2]    = {0, -1};
        const int DOWN[2]  = {0, 1};
};

class Puzzle {
    public:
        static const int SIZE = 4;

    private:
        int id;
        int solution_path_length;
        int positions[SIZE][SIZE];
        int empty_x;
        int empty_y;

    Puzzle();
    string short_state_repr();
    bool swap(int direction[2]);
    void shuffle(int n);

};
