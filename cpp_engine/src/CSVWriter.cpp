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
    // Check whether the file exists and whether it contains data
    std::ifstream checkFile(filename);

    bool needsHeader = true;

    if (checkFile.good())
    {
        checkFile.seekg(0, std::ios::end);

        if (checkFile.tellg() > 0)
        {
            needsHeader = false;
        }
    }

    checkFile.close();

    // Open file in append mode
    std::ofstream file(filename, std::ios::app);

    if (!file.is_open())
    {
        std::cerr << "Error: Unable to open CSV file: "
                  << filename << '\n';
        return;
    }

    // Write header if file is new or empty
    if (needsHeader)
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