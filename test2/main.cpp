#include <iostream>
#include <fstream>
#include <json/json.h>
#include <sstream>
#include "lib_parser.h"

int main() {

    std::ifstream json_file("/home/chen/CLionProjects/test2/complex.json");
    if (!json_file.is_open()) {
        std::cerr << "Unable to open JSON file" << std::endl;
        return 1;
    }

    /*Create a JSON parser*/
    Json::Value json_data;
    Json::CharReaderBuilder json_reader;
    std::string json_errors;
    Json::parseFromStream(json_reader, json_file, &json_data, &json_errors);

    if (!json_errors.empty()) {
        std::cerr << "JSON parsing error: " << json_errors << std::endl;
        return 1;
    }
    LibParser parser;
    /*Root node that stores key-value pairs*/


    parser.traverse_and_store(json_data, parser.content_root);

    parser.my_print(parser.content_root);

    return 0;
}
