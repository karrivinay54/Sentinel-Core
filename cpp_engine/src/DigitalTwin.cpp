#include "../include/DigitalTwin.h"

#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <random>

DigitalTwin::DigitalTwin(const std::string& machineID)
    : machineID(machineID),
      state(MachineState::HEALTHY),
      temperature(36.8),
      vibration(0.32),
      current(3.05),
      voltage(229.6),
      rpm(1498),
      runningTime(0),
      simulationStartTime(std::time(nullptr)),
      generator(std::random_device{}())
{
}

void DigitalTwin::update()
{
    runningTime++;

    std::uniform_real_distribution<double> tempNoise(-0.05, 0.05);
    std::uniform_real_distribution<double> vibrationNoise(-0.01, 0.01);
    std::uniform_real_distribution<double> currentNoise(-0.02, 0.02);
    std::uniform_real_distribution<double> voltageNoise(-0.20, 0.20);
    std::uniform_int_distribution<int> rpmNoise(-1, 1);

    temperature += tempNoise(generator)
                 + RECOVERY_FACTOR * (TARGET_TEMPERATURE - temperature);

    vibration += vibrationNoise(generator)
               + RECOVERY_FACTOR * (TARGET_VIBRATION - vibration);

    current += currentNoise(generator)
             + RECOVERY_FACTOR * (TARGET_CURRENT - current);

    voltage += voltageNoise(generator)
             + RECOVERY_FACTOR * (TARGET_VOLTAGE - voltage);

    rpm += rpmNoise(generator)
         + static_cast<int>(0.10 * (TARGET_RPM - rpm));
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