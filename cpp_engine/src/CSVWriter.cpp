#include "../include/CSVWriter.h"

#include <fstream>

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
         << data.getRPM() << ",";

    switch (record.getMachineState())
    {
        case MachineState::HEALTHY:
            file << "HEALTHY";
            break;

        case MachineState::WARNING:
            file << "WARNING";
            break;

        case MachineState::CRITICAL:
            file << "CRITICAL";
            break;
    }

    file << ",";

    switch (record.getFaultType())
    {
        case FaultType::NONE:
            file << "NONE";
            break;

        case FaultType::BEARING_WEAR:
            file << "BEARING_WEAR";
            break;

        default:
            file << "UNKNOWN";
            break;
    }

    file << '\n';

    file.close();
}