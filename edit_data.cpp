#include <iostream>
#include <fstream>
#include <jsoncpp/json/json.h>

# Version
int MAJOR_VERSION = 0
int MINOR_VERSION = 1
int FIX_VERSION = 9


int main() {
    Json::Value data;
    std::ifstream in("data/abraham_data.json");
    in >> data;

    // Example edit: add/update a key in PARABLES
    data["PARABLES"]["new_parable"]["references"] = "New reference";
    data["PARABLES"]["new_parable"]["verses"] = "New verse text";

    // Save back
    std::ofstream out("data/abraham_data.json");
    out << data;

    std::cout << "Data edited and saved." << std::endl;
    return 0;
}