#include "../include/DigitalTwin.h"

#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <random>
#include <iostream>

DigitalTwin::DigitalTwin(
    const std::string& machineID,
    FaultType fault
)
    : machineID(machineID),
      state(MachineState::HEALTHY),
      assignedFault(fault),
      currentFault(FaultType::NONE),
      temperature(36.8),
      vibration(0.32),
      current(3.05),
      voltage(229.6),
      rpm(1498),
      runningTime(0),
      simulationStartTime(std::time(nullptr)),
      generator(std::random_device{}())
{
    // Initialize operating targets to healthy values
    targetTemperature = HEALTHY_TEMPERATURE;
    targetVibration   = HEALTHY_VIBRATION;
    targetCurrent     = HEALTHY_CURRENT;
    targetVoltage     = HEALTHY_VOLTAGE;
    targetRPM         = HEALTHY_RPM;
}

void DigitalTwin::update()
{
    runningTime++;

    updateState();
    updateFault();
    updateTargets();
    updateSensors();
}

void DigitalTwin::updateState()
{
    if (runningTime < 20)
    {
        state = MachineState::HEALTHY;

        std::cout << "[STATE] HEALTHY\n";
    }
    else
    {
        state = MachineState::WARNING;

        std::cout << "[STATE] WARNING\n";
    }
}

void DigitalTwin::updateFault()
{
    if (state == MachineState::HEALTHY)
    {
        currentFault = FaultType::NONE;
    }
    else
    {
        currentFault = assignedFault;
    }
}

void DigitalTwin::updateTargets()
{
    if (state == MachineState::HEALTHY)
    {
        targetTemperature = HEALTHY_TEMPERATURE;
        targetVibration   = HEALTHY_VIBRATION;
        targetCurrent     = HEALTHY_CURRENT;
        targetVoltage     = HEALTHY_VOLTAGE;
        targetRPM         = HEALTHY_RPM;

        return;
    }

    switch (currentFault)
    {
        case FaultType::BEARING_WEAR:
            targetTemperature = 37.5;
            targetVibration   = 0.48;
            targetCurrent     = 3.20;
            targetVoltage     = HEALTHY_VOLTAGE;
            targetRPM         = 1492;
            break;

        case FaultType::NONE:
        default:
            targetTemperature = HEALTHY_TEMPERATURE;
            targetVibration   = HEALTHY_VIBRATION;
            targetCurrent     = HEALTHY_CURRENT;
            targetVoltage     = HEALTHY_VOLTAGE;
            targetRPM         = HEALTHY_RPM;
            break;
    }
}


void DigitalTwin::updateSensors()
{
    std::uniform_real_distribution<double> tempNoise(-0.05, 0.05);
    std::uniform_real_distribution<double> vibrationNoise(-0.01, 0.01);
    std::uniform_real_distribution<double> currentNoise(-0.02, 0.02);
    std::uniform_real_distribution<double> voltageNoise(-0.20, 0.20);
    std::uniform_int_distribution<int> rpmNoise(-1, 1);

    temperature += tempNoise(generator)
             + RECOVERY_FACTOR * (targetTemperature - temperature);

    vibration += vibrationNoise(generator)
           + RECOVERY_FACTOR * (targetVibration - vibration);

    current += currentNoise(generator)
         + RECOVERY_FACTOR * (targetCurrent - current);

    voltage += voltageNoise(generator)
             + RECOVERY_FACTOR * (targetVoltage - voltage);

    rpm += rpmNoise(generator)
         + static_cast<int>(0.10 * (targetRPM - rpm));
}

SensorData DigitalTwin::generateReading()
{
    std::time_t simulatedTime = simulationStartTime + runningTime;
    std::tm* localTime = std::localtime(&simulatedTime);

    std::ostringstream timestamp;

    timestamp << std::put_time(localTime, "%Y-%m-%d %H:%M:%S");

    return SensorData(
        timestamp.str(),
        machineID,
        temperature,
        vibration,
        current,
        voltage,
        rpm
    );
}

MachineState DigitalTwin::getState() const
{
    return state;
}

FaultType DigitalTwin::getFaultType() const
{
    return currentFault;
}