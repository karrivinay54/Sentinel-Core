#include "../include/DigitalTwin.h"

#include <ctime>
#include <iomanip>
#include <sstream>

DigitalTwin::DigitalTwin(const std::string& machineID)
    : machineID(machineID),
      state(MachineState::HEALTHY)
{
}

SensorData DigitalTwin::generateReading()
{
    // Current timestamp
    std::time_t now = std::time(nullptr);

    std::tm* localTime = std::localtime(&now);

    std::ostringstream timestamp;

    timestamp << std::put_time(localTime, "%Y-%m-%d %H:%M:%S");

    return SensorData(
        timestamp.str(),
        machineID,
        36.8,
        0.32,
        3.05,
        229.6,
        1498
    );
}