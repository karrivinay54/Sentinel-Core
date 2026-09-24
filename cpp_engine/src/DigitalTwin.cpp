#include "../include/DigitalTwin.h"

#include <cmath>
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
      degradationLevel(0.0),
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
    updateDegradation();
    updateState();
    updateFault();
    updateTargets();
    updateSensors();
}

void DigitalTwin::updateState()
{
    if (degradationLevel < 0.40)
    {
        state = MachineState::HEALTHY;
    }
    else if (degradationLevel < 0.70)
    {
        state = MachineState::WARNING;
    }
    else if (degradationLevel < 0.90)
    {
        state = MachineState::FAULT;
    }
    else
    {
        state = MachineState::CRITICAL;
    }

    std::cout << "[STATE] ";

    switch (state)
    {
        case MachineState::HEALTHY:
            std::cout << "HEALTHY";
            break;

        case MachineState::WARNING:
            std::cout << "WARNING";
            break;

        case MachineState::FAULT:
            std::cout << "FAULT";
            break;

        case MachineState::CRITICAL:
            std::cout << "CRITICAL";
            break;

        default:
            std::cout << "UNKNOWN";
            break;
    }

    std::cout << "\n";
}

void DigitalTwin::updateDegradation()
{
    const double DEGRADATION_RATE = 0.02;

    degradationLevel += DEGRADATION_RATE;

    if (degradationLevel > 1.0)
    {
        degradationLevel = 1.0;
    }

    std::cout << "[DEGRADATION] Level: "
              << degradationLevel << "\n";
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
            targetTemperature =
                HEALTHY_TEMPERATURE +
                degradationLevel * (37.5 - HEALTHY_TEMPERATURE);

            targetVibration =
                HEALTHY_VIBRATION +
                degradationLevel * (0.48 - HEALTHY_VIBRATION);

            targetCurrent =
                HEALTHY_CURRENT +
                degradationLevel * (3.20 - HEALTHY_CURRENT);

            targetVoltage = HEALTHY_VOLTAGE;

            targetRPM =
                HEALTHY_RPM +
                static_cast<int>(
                    degradationLevel * (1492 - HEALTHY_RPM)
                );
            break;


        case FaultType::MISALIGNMENT:
            targetTemperature =
                HEALTHY_TEMPERATURE +
                degradationLevel * (37.8 - HEALTHY_TEMPERATURE);

            targetVibration =
                HEALTHY_VIBRATION +
                degradationLevel * (0.65 - HEALTHY_VIBRATION);

            targetCurrent =
                HEALTHY_CURRENT +
                degradationLevel * (3.25 - HEALTHY_CURRENT);

            targetVoltage = HEALTHY_VOLTAGE;

            targetRPM =
                HEALTHY_RPM +
                static_cast<int>(
                    degradationLevel * (1490 - HEALTHY_RPM)
                );
            break;


        case FaultType::COOLING_FAILURE:
            targetTemperature =
                HEALTHY_TEMPERATURE +
                degradationLevel * (42.0 - HEALTHY_TEMPERATURE);

            targetVibration = HEALTHY_VIBRATION;

            targetCurrent =
                HEALTHY_CURRENT +
                degradationLevel * (3.20 - HEALTHY_CURRENT);

            targetVoltage = HEALTHY_VOLTAGE;
            targetRPM = HEALTHY_RPM;
            break;


        case FaultType::OVERLOAD:
            targetTemperature =
                HEALTHY_TEMPERATURE +
                degradationLevel * (39.0 - HEALTHY_TEMPERATURE);

            targetVibration =
                HEALTHY_VIBRATION +
                degradationLevel * (0.40 - HEALTHY_VIBRATION);

            targetCurrent =
                HEALTHY_CURRENT +
                degradationLevel * (4.50 - HEALTHY_CURRENT);

            targetVoltage =
                HEALTHY_VOLTAGE +
                degradationLevel * (225.0 - HEALTHY_VOLTAGE);

            targetRPM =
                HEALTHY_RPM +
                static_cast<int>(
                    degradationLevel * (1450 - HEALTHY_RPM)
                );
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
    + static_cast<int>(
        std::round(0.10 * (targetRPM - rpm))
      );
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

double DigitalTwin::getDegradationLevel() const
{
    return degradationLevel;
}