#ifndef PERCEPTRON_H
#define PERCEPTRON_H

#include<vector>
#include<set>

class Perceptron {
private:
    bool valid;
    std::vector<std::vector<int>> x;
    std::vector<int> y;
    int k;
    std::vector<int> theta;
    int b;
    std::set<int> misclassified;

    void validate();
public:
    Perceptron(const std::vector<std::vector<int>> & x_in, const std::vector<int> & y_in);
    void train();
    bool isValid() const;
    int getK() const;
    std::vector<int> getTheta() const;
    int predict(const std::vector<int> & x) const;
};

#endif // PERCEPTRON_H
