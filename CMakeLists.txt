cmake_minimum_required(VERSION 3.16)

project(PulseWatch_or LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
include(FetchContent)

FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.12.0
    GIT_SHALLOW TRUE
)

FetchContent_MakeAvailable(nlohmann_json)


add_executable(PulseWatch_or main.cpp
    systemmetrics.h systemmetrics.cpp
    csvlogger.h csvlogger.cpp
    jsonserializer.h jsonserializer.cpp
    apiclient.h apiclient.cpp)

target_link_libraries(
    PulseWatch_or
    PRIVATE
    nlohmann_json::nlohmann_json
    winhttp
)

