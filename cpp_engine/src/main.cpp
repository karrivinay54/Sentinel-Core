#include "../include/SimulationManager.h"

#include <cstdio>

int main()
{
    std::remove("cpp_engine/data/sensor_data.csv");

    SimulationConfig config(
        "M001",
        "cpp_engine/data/sensor_data.csv",
        50
    );

    SimulationManager manager(config);

    manager.run();

    return 0;
}