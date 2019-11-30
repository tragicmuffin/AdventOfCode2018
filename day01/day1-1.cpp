// Advent of Code 2018: Day 1, Part 1
// https://adventofcode.com/2018/day/1
// Jesse Williams
// Answer: 587

#include <fstream>
#include <iostream>

int main() {

    std::ifstream input;
    input.open("day1_input.txt");

    int freq = 0;
    int num;
    while (input >> num) {  // passes one 'word' at a time to num
        freq += num;
    }
    std::cout << freq;

    return 0;
}
