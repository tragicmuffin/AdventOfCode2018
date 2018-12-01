// Advent of Code 2018: Day 1, Part 2
// https://adventofcode.com/2018/day/1#part2
// Jesse Williams
// Answer:

#include <fstream>
#include <iostream>

#define listLength 1004

int main() {

    std::ifstream input;
    input.open("day1-1_input.txt");

    int freq = 0;
    int seenFreqs [listLength];
    seenFreqs[0] = 0;
    int i = 1;
    int num;
    while (input >> num) {  // passes one 'word' at a time to num
        freq += num;

        for (int j = 0; j <= i; j++) {
            if (seenFreqs[j] == freq) {
                std::cout << freq;
                return 0;
            }
        }

        seenFreqs[i] = freq;
        i++;
    }

    std::cout << "fuck";
    return 0;
}
