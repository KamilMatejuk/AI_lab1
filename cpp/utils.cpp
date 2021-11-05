#include "utils.h"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

string bold(string text) {
    return "\033[1m" + text + "\033[0m";
}

string red(string text) {
    return "\033[31m" + text + "\033[0m";
}

string green(string text) {
    return "\033[32m" + text + "\033[0m";
}

string cyan(string text) {
    return "\033[36m" + text + "\033[0m";
}


string section_name(string text) {
    int count = 80;
    string res = "";
    if (text.size() > count) {
        res = text; 
    } else {
        int padding = (count - text.size()) / 2;
        for (int i = 0; i < padding - 1; i++) {
            res += "=";
        }
        res += " " + text + " ";
        int size = res.size();
        for (int i = count; i > size; i--) {
            res += "=";
        }
    }
    return bold(green(res));
}

string iteration_name(string text) {
    int count = 80;
    string res = "";
    if (text.size() > count) {
        res = text; 
    } else {
        int padding = (count - text.size()) / 2;
        for (int i = 0; i < padding - 1; i++) {
            res += "=";
        }
        res += " " + text + " ";
        int size = res.size();
        for (int i = count; i > size; i--) {
            res += "=";
        }
    }
    return bold(cyan(res));
}

void clear_log() {
    ofstream outfile;
    outfile.open(LOG_FILE);
    outfile << "";
}

void log(string text) {
    cout << text << endl;
    // remove special chars
    vector<string> remove_list;
    remove_list.push_back("\033[0m");
    remove_list.push_back("\033[1m");
    remove_list.push_back("\033[31m");
    remove_list.push_back("\033[32m");
    remove_list.push_back("\033[36m");
    for (string rs : remove_list) {
        size_t pos = string::npos;
        while ((pos = text.find(rs)) != string::npos) {
            text.erase(pos, rs.length());
        }
    }
    ofstream outfile;
    outfile.open(LOG_FILE, ios_base::app); // append instead of overwrite
    outfile << text + "\n";
}
