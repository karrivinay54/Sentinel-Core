#include "../include/SimulationConfig.h"

// Constructor
SimulationConfig::SimulationConfig(
    int machineCount,
    const std::string& outputFile,
    int numIterations
)
    : machineCount(machineCount),
      outputFile(outputFile),
      numIterations(numIterations)
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