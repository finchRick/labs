#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>

class Income {

public:
    Income () = default;
    virtual void print();
    std::string getSource() { return source;};
    Income (std::string src, int mo);
    virtual ~Income() = default;
    void setSource(std::string s) { source = s;};
    virtual void readline (std::stringstream& ss) = 0;
    
protected:
    std::string source;
    int money;
};

class Salary : public Income {

public:
    Salary () = default;
    Salary (std::string src, int mo, std::string fir, std::string dat) : Income {src, mo}, firm {fir}, date {dat} {};
    ~Salary () = default;
    void print();
    void readline (std::stringstream& ss);
private:
    std::string firm;
    std::string date;
};

class Rent : public Income {

public:
    Rent () {};
    Rent (std::string src, int mo, std::string ten) : Income{src, mo}, tenant{ten} {};
    ~Rent () = default;
    void readline (std::stringstream& ss);
    void print();
private:
    std::string tenant;
};

void Income::print() {
    std::cout  << "Source: " << source << std::endl;
    std::cout  << "Money: " << money << std::endl;
}

void Rent::print() {
    std::cout  << "Type rent: \n";
    Income::print();
    std::cout << "Tenant: " << tenant << std::endl;
}

void Salary::print() {
    std::cout  << "Type salary: \n"; 
    Income::print();
    std::cout << "Firm: " << firm << std::endl << "Date: " << date << std::endl;
}

Income::Income (std::string src, int mo) {
    source = src; 
    money = mo;
};

void Rent::readline (std::stringstream& ss) {

    ss >> source >> money;
    ss >> tenant;

}

void Salary::readline (std::stringstream& ss) {

    ss >> source >> money;
    ss >> firm >> date;
}


int main() {

    std::ifstream ft ("inp.txt");
    std::vector<Income*> line;
    std::string inp;
    while (std::getline (ft, inp)){
        std::stringstream ss(inp);
        Income* ff;
        std::string fWord;
        ss >> fWord;
        if (fWord == "Rent") {
            ff = new Rent;
            ff->readline(ss);
        } else if (fWord == "Salary") {
            ff = new Salary;
            ff->readline(ss);
        }
        line.push_back (ff);
    }

    for (Income* it : line) {
        it->print();
        std::cout << std::endl;
    }
    
    for (auto& it : line) {
        delete it;
    }
}