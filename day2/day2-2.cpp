// Advent of Code 2018: Day 2, Part 2
// https://adventofcode.com/2018/day/2#part2
// Jesse Williams
// Answer: revtaubfniyhsgxdoajwkqilp

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int similarCount(std::string strA, std::string strB) {
    // Checks two strings for similarity and returns number of characters in common.
    if (strA.size() != strB.size()) { return -1; }

    int count = 0;
    for (int i = 0; i < strA.size(); i++) {
        if (strA[i] == strB[i]) {
            count++;  // count characters in common
        }
    }
    return count;
}

std::string removeDiffChar(std::string strA, std::string strB) {
    // Removes characters not in common between two strings and returns only common letters (in order)
    int count = 0;
    std::string outStr = "";
    for (int i = 0; i < strA.size(); i++) {
        if (strA[i] == strB[i]) {
            outStr += strA[i];  // count characters in common
        }
    }
    return outStr;
}


int main() {
    std::ifstream input;
    input.open("day2_input.txt");

    std::vector<std::string> allIDs;
    std::string boxID;
    while (input >> boxID) {  // passes one 'word' at a time
        allIDs.emplace_back(boxID);  // store all words in array
    }

    for (int i = 0; i < allIDs.size(); i++) {
        for (int j = i+1; j < allIDs.size(); j++) {
            if (similarCount(allIDs[i], allIDs[j]) == allIDs[i].size()-1) {
                std::string commonChars = removeDiffChar(allIDs[i], allIDs[j]);
                std::cout << "~ " << allIDs[i] << "\n~ " << allIDs[j] << "\nLetters in common: '" << commonChars << "'";
                return 0;
            }
        }
    }
    input.close();
    return 0;
}
