#include "utils.h"
#include "puzzle.h"
#include "heuristic.h"
#include "solver.h"
#include <iostream>
#include <string>
#include <ctime>
using namespace std;

int main() {
    clear_log();
    srand(time(NULL));
    int number_of_iterations = 1;
    int number_of_heuristics = 3;
    map<string, DataMap> results;

    for (int i = 0; i < number_of_iterations; i++) {
        log(iteration_name("Running test " + to_string(i + 1)));
        log(section_name("Generating random Puzzle 15"));
        // random starting permutation
        Puzzle p = Puzzle();
        p.show();
        // solve with heuristics
        for (int j = 0; j < number_of_heuristics; j++) {
            log(section_name("Testing heuristic " + to_string(j + 1)));
            Solver s = Solver(p);
            s.solve(j + 1);
            string map_key = "heuristic " + to_string(j + 1) + " " + to_string(i);
            results.insert({map_key, s.get_data()});
        }
    }
    log(iteration_name("Comparing results"));
    Solver::compare_results(results, number_of_heuristics);
    return 0;
}