#include <string>
#include <vector>
using namespace std;


enum Direction {
    // angle from vertical
    UP    = 0,
    RIGHT = 90,
    DOWN  = 180,
    LEFT  = 270
};

class Puzzle {
    public:
        static const int SIZE = 4;
        Puzzle();
        string short_state_repr();
        bool swap(Direction direction);
        void shuffle(int n);
        vector<Direction> get_possible_moves();
        bool is_finished();
        void show();
    
    private:
        int id;
        int solution_path_length;
        int positions[SIZE][SIZE];
        int empty_x;
        int empty_y;
};
