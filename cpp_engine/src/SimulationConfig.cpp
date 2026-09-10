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
    if (index < 0 || index >= static_cast<int>(faultAssignments.size()))
    {
        return FaultType::NONE;
    }

    return faultAssignments[index];
}