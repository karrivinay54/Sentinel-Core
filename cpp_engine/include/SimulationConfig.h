#pragma once

#include <string>

class SimulationConfig
{
private:
    std::string machineID;
    std::string outputFile;
    int numIterations;

public:
    SimulationConfig(
        const std::string& machineID,
        const std::string& outputFile,
        int numIterations
    );

    std::string getMachineID() const;
    std::string getOutputFile() const;
    int getNumIterations() const;
};