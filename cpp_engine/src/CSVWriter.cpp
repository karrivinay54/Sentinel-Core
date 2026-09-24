#include "../include/CSVWriter.h"

#include <fstream>
#include <iostream>

// Constructor
CSVWriter::CSVWriter(const std::string& filename)
    : filename(filename)
{
}

void CSVWriter::write(const DatasetRecord& record)
{
    // Check if file already exists
    std::ifstream checkFile(filename);
    bool fileExists = checkFile.good();
    checkFile.close();

    std::ofstream file(filename, std::ios::app);

    // Write header only once
    if (!fileExists)
    {
        file << "Timestamp,"
             << "MachineID,"
             << "Temperature,"
             << "Vibration,"
             << "Current,"
             << "Voltage,"
             << "RPM,"
             << "DegradationLevel,"
             << "State,"
             << "FaultType\n";
    }

    const SensorData& data = record.getSensorData();

    file << data.getTimestamp() << ","
         << data.getMachineID() << ","
         << data.getTemperature() << ","
         << data.getVibration() << ","
         << data.getCurrent() << ","
         << data.getVoltage() << ","
         << data.getRPM() << ","
         << record.getDegradationLevel() << ",";

    // Write Machine State
    switch (record.getMachineState())
    {
        case MachineState::OFF:
            file << "OFF";
            break;

        case MachineState::STARTING:
            file << "STARTING";
            break;

        case MachineState::HEALTHY:
            file << "HEALTHY";
            break;

        case MachineState::WARNING:
            file << "WARNING";
            break;

        case MachineState::FAULT:
            file << "FAULT";
            break;

        case MachineState::CRITICAL:
            file << "CRITICAL";
            break;

        case MachineState::SHUTDOWN:
            file << "SHUTDOWN";
            break;

        default:
            file << "UNKNOWN";
            break;
    }

    file << ",";

    // Write Fault Type
    switch (record.getFaultType())
    {
        case FaultType::NONE:
            file << "NONE";
            break;

        case FaultType::BEARING_WEAR:
            file << "BEARING_WEAR";
            break;

        case FaultType::MISALIGNMENT:
            file << "MISALIGNMENT";
            break;

        case FaultType::COOLING_FAILURE:
            file << "COOLING_FAILURE";
            break;

        case FaultType::OVERLOAD:
            file << "OVERLOAD";
            break;

        default:
            file << "UNKNOWN";
            break;
    }

    file << '\n';
    file.close();
}