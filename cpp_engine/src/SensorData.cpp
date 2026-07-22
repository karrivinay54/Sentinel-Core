#include "../include/SensorData.h"

#include <iostream>
#include <sstream>

// Default constructor
SensorData::SensorData()
    : timestamp(""),
      machineID(""),
      temperature(0.0),
      vibration(0.0),
      current(0.0),
      voltage(0.0),
      rpm(0)
{
}

// Parameterized constructor
SensorData::SensorData(const std::string& timestamp,
                       const std::string& machineID,
                       double temperature,
                       double vibration,
                       double current,
                       double voltage,
                       int rpm)
    : timestamp(timestamp),
      machineID(machineID),
      temperature(temperature),
      vibration(vibration),
      current(current),
      voltage(voltage),
      rpm(rpm)
{
}

// Display sensor data
void SensorData::display() const
{
    std::cout << "Timestamp   : " << timestamp << '\n';
    std::cout << "Machine ID  : " << machineID << '\n';
    std::cout << "Temperature : " << temperature << " deg C\n";
    std::cout << "Vibration   : " << vibration << " mm/s\n";
    std::cout << "Current     : " << current << " A\n";
    std::cout << "Voltage     : " << voltage << " V\n";
    std::cout << "RPM         : " << rpm << '\n';
}

// Convert to CSV format
std::string SensorData::toCSV() const
{
    std::ostringstream csv;

    csv << timestamp << ','
        << machineID << ','
        << temperature << ','
        << vibration << ','
        << current << ','
        << voltage << ','
        << rpm;

    return csv.str();
}