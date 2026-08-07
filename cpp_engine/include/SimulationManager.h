#pragma once

#include "SimulationConfig.h"
#include "DigitalTwin.h"
#include "CSVWriter.h"

class SimulationManager
{
private:
    SimulationConfig config;
    DigitalTwin twin;
    CSVWriter writer;

public:
    explicit SimulationManager(const SimulationConfig& config);

    void run();
};