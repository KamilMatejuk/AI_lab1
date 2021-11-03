#pragma once
#include <vector>
#include <ctime>
#include <map>
using namespace std;

typedef map<string, string> DataMap;

class Solver {
    public:
        vector<Puzzle> visited_states;
        vector<Puzzle> states_to_visit;
        Puzzle solution = Puzzle(0);
        Solver();
        void solve();
        DataMap get_data();

    private:
        int heuristic;
        time_t start_time;
        double solving_time;
};
