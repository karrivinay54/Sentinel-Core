#pragma once

#include <string>

class SensorData
{
private:
    std::string timestamp;
    std::string machineID;

    double temperature;
    double vibration;
    double current;
    double voltage;

    int rpm;

public:
    // Constructors
    SensorData();
    SensorData(const std::string& timestamp,
               const std::string& machineID,
               double temperature,
               double vibration,
               double current,
               double voltage,
               int rpm);

    // Functions
    void display() const;
    std::string toCSV() const;
};