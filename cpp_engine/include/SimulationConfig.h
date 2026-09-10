#pragma once

#include <string>
#include <vector>

#include "FaultType.h"

class SimulationConfig
{
private:
    int machineCount;
    std::string outputFile;
    int numIterations;
    std::vector<FaultType> faultAssignments;

public:
    SimulationConfig(
        int machineCount,
        const std::string& outputFile,
        int numIterations,
        const std::vector<FaultType>& faultAssignments
    );

    int getMachineCount() const;
    std::string getOutputFile() const;
    int getNumIterations() const;

    FaultType getFaultForMachine(int index) const;
};