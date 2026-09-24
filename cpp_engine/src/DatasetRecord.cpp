#include "../include/DatasetRecord.h"

DatasetRecord::DatasetRecord(
    const SensorData& sensorData,
    double degradationLevel,
    MachineState machineState,
    FaultType faultType)
    : sensorData(sensorData),
      degradationLevel(degradationLevel),
      machineState(machineState),
      faultType(faultType)
{
}

SensorData DatasetRecord::getSensorData() const
{
    return sensorData;
}

double DatasetRecord::getDegradationLevel() const
{
    return degradationLevel;
}

MachineState DatasetRecord::getMachineState() const
{
    return machineState;
}

FaultType DatasetRecord::getFaultType() const
{
    return faultType;
}