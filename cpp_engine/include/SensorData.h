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
    SensorData();

    SensorData(
        const std::string& timestamp,
        const std::string& machineID,
        double temperature,
        double vibration,
        double current,
        double voltage,
        int rpm
    );

    std::string getTimestamp() const;
    std::string getMachineID() const;

    double getTemperature() const;
    double getVibration() const;
    double getCurrent() const;
    double getVoltage() const;

    int getRPM() const;

    void display() const;

    std::string toCSV() const;
};