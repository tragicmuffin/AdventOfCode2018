// Advent of Code 2018: Day 3, Part 1
// https://adventofcode.com/2018/day/3
// Jesse Williams

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <tuple>

#define fabricWidth 1000
#define fabricHeight 1000

bool doesClaimOccupy(int X, int Y, int W, int H, tuple<int, int> coords) {
    // Check if claim occupies these coords

}

int numberOfClaims(tuple<int, int> coords) {
    for (std::string claim : allClaims) {
        // Parse claim string


        // Check claim
        doesClaimOccupy(X, Y, W, H, coords)
    }
}

int main() {

    std::ifstream input;
    input.open("day3_input.txt");

    std::string claim;
    std::vector<std::string> allClaims;
    while (std::getline(input, claim))
    {
        allClaims.emplace_back(claim);  // store all lines in array
    }

    // Claim format: '#N @ X,Y: WxH'


    tuple<int, int> coords;
    coords = make_tuple(2, 3);


    // Check all fabric coords
    for (int y = 0; y < fabricHeight; y++) {
        for (int x = 0; x < fabricWidth; x++) {

        }
    }

    return 0;
}
