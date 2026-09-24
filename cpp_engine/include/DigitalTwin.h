#pragma once

#include <random>
#include <string>
#include <ctime>

#include "MachineState.h"
#include "SensorData.h"
#include "FaultType.h"

class DigitalTwin
{
private:
    // Machine identity
    std::string machineID;
    MachineState state;
    FaultType assignedFault;
    FaultType currentFault;

    // Current sensor values
    double temperature;
    double vibration;
    double current;
    double voltage;
    int rpm;

   // Simulation
int runningTime;
double degradationLevel;
std::time_t simulationStartTime;
std::mt19937 generator;

    // Healthy operating points
    static constexpr double HEALTHY_TEMPERATURE = 36.8;
    static constexpr double HEALTHY_VIBRATION   = 0.32;
    static constexpr double HEALTHY_CURRENT     = 3.05;
    static constexpr double HEALTHY_VOLTAGE     = 229.6;
    static constexpr int    HEALTHY_RPM         = 1498;

    // Recovery
    static constexpr double RECOVERY_FACTOR = 0.05;

    // Current operating targets
    double targetTemperature;
    double targetVibration;
    double targetCurrent;
    double targetVoltage;
    int targetRPM;

    // Internal helpers
    void updateState();
    void updateFault();
    void updateDegradation();
    void updateTargets();
    void updateSensors();

public:
    DigitalTwin(
    const std::string& machineID,
    FaultType fault
);

    void update();

    SensorData generateReading();

    MachineState getState() const;
    FaultType getFaultType() const;
    double getDegradationLevel() const;
};