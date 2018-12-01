// Advent of Code 2018: Day 1, Part 2
// https://adventofcode.com/2018/day/1#part2
// Jesse Williams
// Answer: 83130

#include <fstream>
#include <iostream>
#include <vector>

int main() {

    std::ifstream input;

    int num;
    int freq = 0;
    std::vector<int> seenFreqs;
    seenFreqs.emplace_back(0);
    while (true) {  // loops through file until a match is found
        input.open("day1-1_input.txt");

        while (input >> num) {  // passes one 'word' at a time to num
            freq += num;

            for (auto j = seenFreqs.begin(); j != seenFreqs.end(); ++j) {
                if (*j == freq) {
                    std::cout << freq;
                    return 0;
                }
            }

            seenFreqs.emplace_back(freq);
        }

        input.close();
    }

    return 0;
}
