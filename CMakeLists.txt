cmake_minimum_required(VERSION 3.16)

project(PulseWatch_or LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(PulseWatch_or main.cpp
    systemmetrics.h systemmetrics.cpp
    csvlogger.h csvlogger.cpp)


