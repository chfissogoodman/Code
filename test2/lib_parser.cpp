#include "lib_parser.h"
#include <iostream>
#include <json/json.h>
#include <sstream>

std::string LibParser:: format_value(const Json::Value& value) {
    std::ostringstream stream;
    if (value.isDouble()) {
        stream << std::fixed << value.asDouble();
    } else {
        stream << value;
    }
    return stream.str();
}

void LibParser::traverse_and_store(const Json::Value& json_data, pair_t& result) {
    if (json_data.isObject()) {
        const auto member_names = json_data.getMemberNames();
        for (const auto& key : member_names) {
            pair_t child;
            traverse_and_store(json_data[key], child);
            result.content_child.push_back(std::make_pair(key, child));
        }
    } else if (json_data.isArray()) {
        for (Json::ArrayIndex index = 0; index < json_data.size(); ++index) {
            pair_t child;
            traverse_and_store(json_data[index], child);
            result.content_child.push_back(std::make_pair(std::to_string(index), child));
        }
    } else {
        result.value = json_data;
    }
}

void LibParser:: my_print(const pair_t& key_value, const std::string& name) {
    if (!key_value.content_child.empty()) {
        for (const auto& pair : key_value.content_child) {
            std::cout << "[" << name << pair.first << ": ";
            my_print(pair.second, name);
        }
    } else {
        std::cout << name << "Value: " << format_value(key_value.value) << "]" << std::endl;
    }
}


