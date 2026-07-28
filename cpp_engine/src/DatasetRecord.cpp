#include "../include/DatasetRecord.h"

DatasetRecord::DatasetRecord(
    const SensorData& sensorData,
    MachineState machineState,
    FaultType faultType)
    : sensorData(sensorData),
      machineState(machineState),
      faultType(faultType)
{
}

SensorData DatasetRecord::getSensorData() const
{
    return sensorData;
}

MachineState DatasetRecord::getMachineState() const
{
    return machineState;
}

FaultType DatasetRecord::getFaultType() const
{
    return faultType;
}