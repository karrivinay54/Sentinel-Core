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

    static constexpr double TARGET_TEMPERATURE = 36.8;
    static constexpr double TARGET_VIBRATION   = 0.32;
    static constexpr double TARGET_CURRENT     = 3.05;
    static constexpr double TARGET_VOLTAGE     = 229.6;
    static constexpr int    TARGET_RPM         = 1498;

static constexpr double RECOVERY_FACTOR    = 0.05;

    std::time_t simulationStartTime;

    std::mt19937 generator;

public:
    explicit DigitalTwin(const std::string& machineID);

    void update();

    SensorData generateReading();
};