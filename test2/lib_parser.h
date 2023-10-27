#ifndef LIB_PARSER_H
#define LIB_PARSER_H

#include <json/json.h>
#include <string>
#include <vector>
class LibParser{
public:
struct pair_t {
    std::vector<std::pair<std::string, pair_t>> content_child;
    Json::Value value;
};

std::string format_value(const Json::Value& value);

void traverse_and_store(const Json::Value& json_data, pair_t& result);

void my_print(const pair_t& key_value, const std::string& name = "");

pair_t content_root;

};
#endif  // LIB_PARSER_H
