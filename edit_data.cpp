#include <iostream>
#include <fstream>
#include <jsoncpp/json/json.h>

# Version
int MAJOR_VERSION = 0
int MINOR_VERSION = 1
int FIX_VERSION = 8


int main() {
    Json::Value data;
    std::ifstream in("data/data.json");
    in >> data;

    // Example edit: add/update a key in PARABLES
    data["PARABLES"]["new_parable"]["references"] = "New reference";
    data["PARABLES"]["new_parable"]["verses"] = "New verse text";

    // Save back
    std::ofstream out("data/data.json");
    out << data;

    std::cout << "Data edited and saved." << std::endl;
    return 0;
}