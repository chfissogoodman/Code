cmake_minimum_required(VERSION 3.26)
project(test2)

set(CMAKE_CXX_STANDARD 17)

add_executable(test2 main.cpp
        lib_parser.cpp
        lib_parser.h
)
link_directories(/usr/local/lib)
set(jsoncpp_lib libjsoncpp.a)
target_link_libraries(test2 ${jsoncpp_lib})