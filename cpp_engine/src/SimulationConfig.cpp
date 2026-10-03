#include "../include/SimulationConfig.h"

// Constructor
SimulationConfig::SimulationConfig(
    int machineCount,
    const std::string& outputFile,
    int numIterations,
    const std::vector<FaultType>& faultAssignments
)
    : machineCount(machineCount),
      outputFile(outputFile),
      numIterations(numIterations),
      faultAssignments(faultAssignments)
{
}

// Getter for Machine Count
int SimulationConfig::getMachineCount() const
{
    return machineCount;
}

// Getter for Output File
std::string SimulationConfig::getOutputFile() const
{
    return outputFile;
}

// Getter for Number of Iterations
int SimulationConfig::getNumIterations() const
{
    return numIterations;
}

// Get fault assigned to a machine
FaultType SimulationConfig::getFaultForMachine(int index) const
{
    if (faultAssignments.empty())
    {
        return FaultType::NONE;
    }

    // Cycle through the configured fault scenarios.
    // This allows multiple machines to share the same
    // fault scenario while retaining independent baselines.
    return faultAssignments[index % faultAssignments.size()];
}