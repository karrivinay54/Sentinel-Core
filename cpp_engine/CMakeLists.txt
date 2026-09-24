cmake_minimum_required(VERSION 3.15)

project(SentinelCore)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(sentinel
    src/main.cpp
    src/DigitalTwin.cpp
    src/SensorData.cpp
    src/DatasetRecord.cpp
    src/CSVWriter.cpp
    src/SimulationConfig.cpp
    src/SimulationManager.cpp
)