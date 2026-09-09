#pragma once

#include <vector>

#include "SimulationConfig.h"
#include "DigitalTwin.h"
#include "CSVWriter.h"

class SimulationManager
{
private:
    SimulationConfig config;
    std::vector<DigitalTwin> twins;
    CSVWriter writer;

public:
    explicit SimulationManager(const SimulationConfig& config);

    void run();
};