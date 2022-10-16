#include "perceptron.hpp"
#include<string>
#include<iostream>
#include<vector>

using namespace std;

int main() {
    cout << "Starting perceptron..." << endl;

    vector<vector<int>> x = {
        {1, 1},
        {-3, 2},
        {2, 3},
        {-1, -1},
        {-1, -4},
        {-3, 3},
    };

    vector<int> y = { -1, 1, 1, 1, -1, 1 };
    Perceptron percep(x, y);

    percep.train();

    int k = percep.getK();
    vector<int> theta = percep.getTheta();

    cout << k << ": ";
    for (int i : theta) {
        cout << i << " ";
    }
    cout << endl;

    cout << "Done!" << endl;
}