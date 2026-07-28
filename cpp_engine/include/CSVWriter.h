#pragma once

#include <string>
#include "SensorData.h"
#include "DatasetRecord.h"

class CSVWriter
{
private:
    std::string filename;

public:
    explicit CSVWriter(const std::string& filename);

    void writeData(const SensorData& data);
    void write(const DatasetRecord& record);
};