#include "puzzle.h"
#include <iostream>
#include <string>

class Puzzle
{
public:
  static const int SIZE = 4;

private:
  int solution_path_length;
  int positions[SIZE][SIZE];

  Puzzle()
  {
    // positions = new int[SIZE][SIZE]{ 1};
    for (int i = 0; i < SIZE; i++)
    {
      /* code */
    }

    positions = {1};
  }
};
