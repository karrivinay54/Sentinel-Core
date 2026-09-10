#include "../include/SimulationConfig.h"
#include "../include/SimulationManager.h"
#include "../include/FaultType.h"


#include <cstdio>
#include <vector>

int main()
{
    std::remove("cpp_engine/data/sensor_data.csv");

    std::vector<FaultType> faults =
    {
        FaultType::BEARING_WEAR,
        FaultType::MISALIGNMENT,
        FaultType::COOLING_FAILURE
    };

    SimulationConfig config(
        3,
        "cpp_engine/data/sensor_data.csv",
        50,
        faults
    );

    SimulationManager manager(config);

    manager.run();

    return 0;
}