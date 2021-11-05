#include "puzzle.h"
#include "heuristic.h"
#include "solver.h"
#include <algorithm>
#include <iostream>
#include <string>
#include <limits>
#include <ctime>

Solver::Solver(Puzzle& puzzle) {
    visited_states = {};
    states_to_visit = { puzzle };
    start_time = clock();
}

int Solver::heuristic(int number_of_heuristic, Puzzle& puzzle) {
    switch(number_of_heuristic) {
        case 1: return heuristic1(puzzle);
        case 2: return heuristic2(puzzle);
        default: return 0;
    }
}

void Solver::solve(int number_of_heuristic) {
    // TODO DLACZEGO NIE DZIAŁA DLA WIEKSZYCH ROZMIARÓW
    start_time = clock();
    while (states_to_visit.size() != 0) {
        // find nodes with least f
        int min_index = -1;
        int min_f = numeric_limits<int>::max();
        int min_g = numeric_limits<int>::max();
        int min_h = numeric_limits<int>::max();
        Puzzle min_state = Puzzle();
        for (int i = 0; i < states_to_visit.size(); i++) {
            Puzzle state = states_to_visit[i];
            int h = heuristic(number_of_heuristic, state);
            int g = state.solution_path.size();
            int f = g + h;
            if (f < min_f) {
                min_f = f;
                min_g = g;
                min_h = h;
                min_index = i;
                min_state = state;
            }
        }
        cout << "Found minimal state " << min_state.short_state_repr() << \
                " -> f = g + h = " << min_g << " + " << min_h << " = " << \
                min_f << " " << endl;
        // pop off list
        if (min_index != -1) {
            states_to_visit.erase(states_to_visit.begin() + min_index);
        }
        // for each successor
        for (Direction move : min_state.get_possible_moves()) {
            Puzzle succ = min_state.copy();
            succ.swap(move);
            // check if finished
            if (succ.is_finished()) {
                solution = succ;
                solving_time = ((double) (clock() - start_time)) / CLOCKS_PER_SEC;
                cout << "Found final solution in " << solving_time << " s (path length: " << solution.solution_path.size() << ")" << endl;
                for (Direction d : solution.solution_path) {
                    cout << get_direction_name(d) + " ";
                }
                cout << endl;
                return;
            }
            // f = g + h
            int succ_f = succ.solution_path.size() + heuristic(number_of_heuristic, succ);
            // check if already in list to visit with lower value
            bool already_exists_with_lower_f = false;
            for (Puzzle state : states_to_visit) {
                if (state.short_state_repr() == succ.short_state_repr()) {
                    int state_f = state.solution_path.size() + heuristic(number_of_heuristic, state);
                    if (state_f < succ_f) {
                        already_exists_with_lower_f = true;
                        break;
                    }
                }
            }
            if (already_exists_with_lower_f) {
                continue;
            }
            // check if already visited with lower value
            already_exists_with_lower_f = false;
            for (Puzzle state : visited_states) {
                if (state.short_state_repr() == succ.short_state_repr()) {
                    int state_f = state.solution_path.size() + heuristic(number_of_heuristic, state);
                    if (state_f < succ_f) {
                        already_exists_with_lower_f = true;
                        break;
                    }
                }
            }
            if (already_exists_with_lower_f) {
                continue;
            }
            // otherwise add to list
            states_to_visit.push_back(succ);
        }
        visited_states.push_back(min_state);
    }
}

DataMap Solver::get_data() {
    string path = "";
    for (Direction d : solution.solution_path) {
        path += get_direction_name(d) + " ";
    }
    if (solving_time == 0) {
        solving_time = ((double) (clock() - start_time)) / CLOCKS_PER_SEC;
    }
    return {
        {"number of visited states", to_string(visited_states.size() + 1)},
        {"path length", to_string(solution.solution_path.size())},
        {"path", path},
        {"time", to_string(solving_time)}
    };
}
