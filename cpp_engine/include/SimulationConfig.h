#pragma once

#include <string>

class SimulationConfig
{
private:
    int machineCount;
    std::string outputFile;
    int numIterations;

public:
    SimulationConfig(
        int machineCount,
        const std::string& outputFile,
        int numIterations
    );

    int getMachineCount() const;
    std::string getOutputFile() const;
    int getNumIterations() const;
};