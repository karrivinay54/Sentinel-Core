#ifndef DATASET_RECORD_H
#define DATASET_RECORD_H

#include "SensorData.h"
#include "MachineState.h"
#include "FaultType.h"

class DatasetRecord
{
private:
    SensorData sensorData;
    MachineState machineState;
    FaultType faultType;

public:
    DatasetRecord(
        const SensorData& sensorData,
        MachineState machineState,
        FaultType faultType
    );

    SensorData getSensorData() const;

    MachineState getMachineState() const;

    FaultType getFaultType() const;
};

#endif