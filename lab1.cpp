#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>

class Income {

public:
    virtual void print();
    std::string getSource() { return source;};
    Income (std::string src, int mo);
    virtual ~Income() = default;
    void setSource(std::string s) { source = s;};
    
private:
    std::string source;
protected:
    int money;
};

class Salary : public Income {

public:
    Salary (std::string src, int mo, std::string fir, std::string dat) : Income {src, mo}, firm {fir}, date {dat} {};
    ~Salary () = default;
    void print();
private:
    std::string firm;
    std::string date;
};

class Rent : public Income {

public:
    Rent (std::string src, int mo, std::string ten) : Income{src, mo}, tenant{ten} {};
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


int main() {

    std::ifstream ft ("inp.txt");
    std::vector<Income*> line;
    std::string inp;
    while (std::getline (ft, inp)){
        std::string singlWord;
        int i=0;
        for (; i<inp.length(); i++) {
            if (inp[i] == ' ') break;
            singlWord.push_back(inp[i]); 
        }
        if (singlWord == "Rent") {
            std::string src, ten, mon;
            int mo;
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                src.push_back(inp[i]);
            }
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                mon.push_back(inp[i]);
            }
            mo = std::stoi(mon);
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                ten.push_back(inp[i]);
            }
            Income* fin = new Rent(src, mo, ten);
            line.push_back(fin);
        } else if (singlWord == "Salary") {
            std::string src, mon, fir, dat;
            int mo;
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                src.push_back(inp[i]);
            }
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                mon.push_back(inp[i]);
            }
            mo = std::stoi(mon);
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                fir.push_back(inp[i]);
            }
            i++;
            for (;i<inp.length(); i++) {
                if (inp[i] == ' ') break;;
                dat.push_back(inp[i]);
            }
            Income* fin = new Salary(src, mo, fir, dat);
            line.push_back(fin);
        }
    }

    for (auto& it : line) {
        it->print();
        std::cout << std::endl;
    }
    
    for (auto& it : line) {
        delete it;
    }
}