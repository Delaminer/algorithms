#include "perceptron.hpp"
#include<vector>
#include<algorithm>
#include<numeric>
#include<random>

using namespace std;

int sign(int x) {
  if (x > 0) return 1;
  if (x < 0) return -1;
  return 0;
}

Perceptron::Perceptron(const vector<vector<int>> & x_in, const vector<int> & y_in) : valid(false), x(x_in), y(y_in), k(0), b(0) {
    theta.resize(x_in[0].size());
    validate();
}

void Perceptron::validate() {

    misclassified.clear();

    for (int i = 0; i < x.size(); ++i) {
        // Is x_i properly classified?
        vector<int> & x_i = x[i];
        int & y_i = y[i];

        // We need y_i = theta * x_i
        int product = inner_product(theta.begin(), theta.end(), x_i.begin(), 0);
        if (product != y_i) {
            // Improperly classified!
            misclassified.insert(i);
        }
    }


    valid = misclassified.empty();
}

void Perceptron::train() {
    
    // Do calculations

    k = 0;
    valid = false;
    fill(theta.begin(), theta.end(), 0);

    vector<int> indices(x.size());
    iota(indices.begin(), indices.end(), 0);

    while (!valid) {
        valid = true;

        shuffle(indices.begin(), indices.end(), mt19937{random_device{}()});
        for (int i : indices) {
            vector<int> & x_i = x[i];
            int & y_i = y[i];

            // We need y_i = sign(theta * x_i)
            int product = sign(inner_product(theta.begin(), theta.end(), x_i.begin(), 0));
            if (product != y_i) {
                // Improperly classified!
                valid = false;

                // Theta += y_i * x_i

                // Get y_i * x_i
                transform(x_i.begin(), x_i.end(), x_i.begin(), [&y_i](auto& x_ij){ return y_i * x_ij; });

                // Get theta += y_i * x_i
                transform(theta.begin(), theta.end(), x_i.begin(), theta.begin(), plus<double>());

                // Get x_i
                transform(x_i.begin(), x_i.end(), x_i.begin(), [&y_i](auto& x_ij){ return x_ij / y_i; });

                k++;
            }
        }
    }
}

bool Perceptron::isValid() const {
    return valid;
}

int Perceptron::getK() const {
    return k;
}

vector<int> Perceptron::getTheta() const {
    return theta;
}

int Perceptron::predict(const vector<int> & x) const {
    // y = theta * x
    return inner_product(theta.begin(), theta.end(), x.begin(), 0);
}