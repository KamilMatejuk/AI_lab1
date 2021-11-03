#include "puzzle.h"
#include "heuristic.h"
#include "solver.h"
#include "utils.h"
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    // TODO dodać logi
    int number_of_iterations = 1;
    int number_of_heuristics = 2;
    map<string, DataMap> results;

    Puzzle p = Puzzle();
    p.show();
    return 0;
    
    for (int i = 0; i < number_of_iterations; i++) {
        cout << iteration_name("Running test " + to_string(i + 1)) << endl;
        cout << section_name("Generating random Puzzle 15") << endl;
        // random starting permutation
        Puzzle p = Puzzle(i + 1);
        p.show();
        // solve with heuristics
        for (int j = 0; j < number_of_heuristics; j++) {
            cout << section_name("Testing heuristic " + to_string(j + 1)) << endl;
            Solver s = Solver(p);
            s.solve(j);
            results.insert({"heuristic " + to_string(j + 1), s.get_data()});
        }
    }
    cout << iteration_name("Comparing results") << endl;
    for (auto const& x : results) {
        string heuristic_name = x.first;
        DataMap data = x.second;
    }
    return 0;
}