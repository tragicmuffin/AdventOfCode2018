// Advent of Code 2018: Day 2, Part 1
// https://adventofcode.com/2018/day/2
// Jesse Williams
// Answer: 6225

#include <fstream>
#include <iostream>
#include <string>

int main() {

    std::ifstream input;
    input.open("day2_input.txt");

    int doubles = 0;
    int triples = 0;

    std::string boxID;
    while (input >> boxID) {  // passes one 'word' at a time
        // check str for repeated letters
        bool f_double = false;
        bool f_triple = false;

        for (auto ch : boxID) {  // for each char (in order) in string
            int count = 0;
            for (auto o : boxID) {  // count how many times char appears in string
                if (ch == o) {
                    count += 1;  // should always be at least 1
                }
            }
            if (count == 2) {
                f_double = true;
            }
            if (count == 3) {
                f_triple = true;
            }
        }

        if (f_double) { doubles += 1; }
        if (f_triple) { triples += 1; }
    }

    input.close();
    std::cout << doubles << " * " << triples << " = " << (doubles*triples) << "\n";

    return 0;
}
