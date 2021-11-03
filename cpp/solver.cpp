#include "puzzle.h"
#include "heuristic.h"
#include "solver.h"
#include <algorithm>
#include <iostream>
#include <string>
#include <limits>

Solver::Solver(Puzzle puzzle) {
    visited_states = {};
    states_to_visit = { puzzle };
}

int Solver::heuristic(int number_of_heuristic, Puzzle puzzle) {
    switch(number_of_heuristic) {
        case 1: return heuristic1(puzzle);
        case 2: return heuristic2(puzzle);
        default: return 0;
    }
}

void Solver::solve(int number_of_heuristic) {
    time(&start_time);
    while (states_to_visit.size() != 0) {
        // find nodes with least f
        int min_f = numeric_limits<int>::infinity();
        Puzzle min_state = Puzzle();
        for (Puzzle state : states_to_visit) {
            int h = heuristic(number_of_heuristic, state);
            int g = state.solution_path.size();
            int f = g + h;
            if (f < min_f) {
                min_f = f;
                min_state = state;
            }
        }
        cout << "Found minimal state " << min_state.short_state_repr() << \
                " -> f = g + h = " << min_f << endl;
        // pop off list
        int index = -1;
        for (int i = 0; i < states_to_visit.size(); i++) {
            if (states_to_visit[i] == min_state) {
                index = i;
            }
        }
        if (index != -1) {
            states_to_visit.erase(states_to_visit.begin() + index);
        }
        // for each successor
        for (Direction move : min_state.get_possible_moves()) {
            Puzzle succ = min_state.copy();
            succ.swap(move);
            // check if finished
            if (succ.is_finished()) {
                solution = succ;
                time_t end_time;
                time(&end_time);
                solving_time = end_time - start_time;
                cout << "Found final solution in" << solving_time << " (" << solution.solution_path.size() << ")" << endl;
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
    return {
        {"number of visited states", to_string(visited_states.size())},
        {"path length", to_string(solution.solution_path.size())},
        {"path", path},
        {"time", to_string(solving_time)}
    };
}
