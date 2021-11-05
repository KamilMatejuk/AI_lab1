#pragma once
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <ctime>
#include <map>

typedef map<string, string> DataMap;

template<typename T> static void show_data(string name, vector<T> v) {
    string values = bold(cyan(name)) + " [ ";
    for (T vs : v) {
        values += to_string(vs) + " ";
    }
    values += "]";
    log(values);
    log(bold("\taverage:       ") + to_string(avg(v)));
    log(bold("\tmedian:        ") + to_string(median(v)));
    log(bold("\tstd deviation: ") + to_string(standard_deviation(v)));
}
template static void show_data(string, vector<int>);
template static void show_data(string, vector<double>);

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

        static void compare_results(map<string, DataMap> results, int number_of_heuristics) {
            for (int j = 0; j < number_of_heuristics; j++) {
                vector<int> numbers_of_visited_states;
                vector<int> path_lengths;
                vector<double> times;
                string heuristic_key = "heuristic " + to_string(j + 1);
                for (auto const& x : results) {
                    string heuristic_name = x.first;
                    // if this is data for this heuristic
                    if (heuristic_name.find(heuristic_key) != string::npos) {
                        DataMap data = x.second;
                        for (auto const& d : data) {
                            string key = d.first;
                            string value = d.second;
                            if (key == "number of visited states") {
                                numbers_of_visited_states.push_back(atoi(value.c_str()));
                            }
                            if (key == "path length") {
                                path_lengths.push_back(atoi(value.c_str()));
                            }
                            if (key == "time") {
                                times.push_back(stod(value, NULL));
                            }
                        }
                    }
                }

                log(bold(red(heuristic_key)));
                show_data("Visited states", numbers_of_visited_states);
                show_data("Path lengths  ", path_lengths);
                show_data("Duration      ", times);
            }
        }

};
