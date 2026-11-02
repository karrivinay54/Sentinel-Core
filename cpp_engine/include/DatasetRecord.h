#pragma once

#include "SensorData.h"
#include "MachineState.h"
#include "FaultType.h"

class DatasetRecord
{
private:
    SensorData sensorData;
    double degradationLevel;
    MachineState machineState;
    FaultType faultType;

public:
    DatasetRecord(
        const SensorData& sensorData,
        double degradationLevel,
        MachineState machineState,
        FaultType faultType
    );

    SensorData getSensorData() const;
    double getDegradationLevel() const;
    MachineState getMachineState() const;
    FaultType getFaultType() const;
};