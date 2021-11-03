#include "puzzle.h"
#include "solver.h"
#include "utils.h"
#include <iostream>
#include <string>

using namespace std;

int main() {
    int number_of_iterations = 1;
    for (int i = 0; i < number_of_iterations; i++) {
        cout << iteration_name("Running test " + to_string(i + 1)) << endl;
        cout << section_name("Generating random Puzzle 15") << endl;
        // random starting permutation
        Puzzle p = Puzzle(i + 1);
        p.show();
        // solve with heuristics
        
    }
    
    Puzzle p = Puzzle(1);
    p.show();
    cout << p.is_finished() << endl;
    p.shuffle(10);
    p.show();
    cout << p.is_finished() << endl;
    return 0;
}