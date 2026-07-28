#include "../include/CSVWriter.h"

#include <fstream>

// Constructor
CSVWriter::CSVWriter(const std::string& filename)
    : filename(filename)
{
}

void CSVWriter::writeData(const SensorData& data)
{
    // Check if the file already exists
    std::ifstream checkFile(filename);

    bool fileExists = checkFile.good();

    checkFile.close();

    std::ofstream file(filename, std::ios::app);

    if (!fileExists)
    {
        file << "Timestamp,"
             << "MachineID,"
             << "Temperature,"
             << "Vibration,"
             << "Current,"
             << "Voltage,"
             << "RPM\n";
    }

    file << data.toCSV() << '\n';

    file.close();
}

void CSVWriter::write(const DatasetRecord& record)
{
    writeData(record.getSensorData());
}