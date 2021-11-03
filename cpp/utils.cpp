#include "utils.h"
#include <curses.h>
#include <string>


string bold(string text) {
    return "\033[1m" + text + "\033[0m";
}

string green(string text) {
    return "\033[32m" + text + "\033[0m";
}

string cyan(string text) {
    return "\033[36m" + text + "\033[0m";
}


string section_name(string text) {
    int count = 30;
    string res = "";
    for (int i = 0; i < count; i++) {
        res += "=";
    }
    res += " " + text + " ";
    for (int i = 0; i < count; i++) {
        res += "=";
    }
    return bold(green(res));
}

string iteration_name(string text) {
    int count = 30;
    string res = "";
    for (int i = 0; i < count; i++) {
        res += "=";
    }
    res += " " + text + " ";
    for (int i = 0; i < count; i++) {
        res += "=";
    }
    return bold(cyan(res));
}
