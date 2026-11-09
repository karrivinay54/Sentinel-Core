
#include "../include/SimulationConfig.h"
#include "../include/SimulationManager.h"
#include "../include/FaultType.h"

#include <cstdio>
#include <string>
#include <vector>

int main(int argc, char* argv[])
{
    std::vector<FaultType> faults =
    {
        FaultType::NONE,
        FaultType::BEARING_WEAR,
        FaultType::MISALIGNMENT,
        FaultType::COOLING_FAILURE,
        FaultType::OVERLOAD
    };

    // Use the supplied output path or the existing default.
    std::string outputFile =
        (argc > 1)
        ? argv[1]
        : "cpp_engine/data/integration_test.csv";

    SimulationConfig config(
        5,
        outputFile,
        120,
        faults
    );

    SimulationManager manager(config);
    manager.run();

    return 0;
}
