#include "../include/SimulationConfig.h"
#include "../include/SimulationManager.h"
#include "../include/FaultType.h"


#include <cstdio>
#include <vector>

int main()
{
    std::vector<FaultType> faults =
{
    FaultType::NONE,
    FaultType::BEARING_WEAR,
    FaultType::MISALIGNMENT,
    FaultType::COOLING_FAILURE,
    FaultType::OVERLOAD
};

SimulationConfig config(
    20,
    "cpp_engine/data/sensor_data_v2.csv",
    50,
    faults
);

    SimulationManager manager(config);

    manager.run();

    return 0;
}