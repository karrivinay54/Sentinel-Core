#pragma once

#include <random>
#include <string>
#include <ctime>

#include "MachineState.h"
#include "SensorData.h"

class DigitalTwin
{
private:
    std::string machineID;
    MachineState state;

    double temperature;
    double vibration;
    double current;
    double voltage;
    int rpm;

    int runningTime;

    std::time_t simulationStartTime;

    std::mt19937 generator;

public:
    explicit DigitalTwin(const std::string& machineID);

    void update();

    SensorData generateReading();
};