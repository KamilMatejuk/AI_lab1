#pragma once
#include <vector>
#include <ctime>
#include <map>

typedef map<string, string> DataMap;

class Solver {
    public:
        vector<Puzzle> visited_states;
        vector<Puzzle> states_to_visit;
        Puzzle solution;
        double solving_time = 0;
        clock_t start_time;
        
        Solver(Puzzle& puzzle);
        int heuristic(int number_of_heuristic, Puzzle& puzzle);
        void solve(int number_of_heuristic);
        DataMap get_data();
};
