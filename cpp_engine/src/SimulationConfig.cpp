#include "../include/SimulationConfig.h"

// Constructor
SimulationConfig::SimulationConfig(
    const std::string& machineID,
    const std::string& outputFile,
    int numIterations)
    : machineID(machineID),
      outputFile(outputFile),
      numIterations(numIterations)
{
}

// Getter for Machine ID
std::string SimulationConfig::getMachineID() const
{
    return machineID;
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