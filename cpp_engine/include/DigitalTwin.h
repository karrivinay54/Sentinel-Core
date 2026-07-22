#pragma once

#include <string>

#include "MachineState.h"
#include "SensorData.h"

class DigitalTwin
{
private:
    std::string machineID;
    MachineState state;

public:
    explicit DigitalTwin(const std::string& machineID);

    SensorData generateReading();
};