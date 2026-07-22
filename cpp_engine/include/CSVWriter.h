#pragma once

#include <string>
#include "SensorData.h"

class CSVWriter
{
private:
    std::string filename;

public:
    explicit CSVWriter(const std::string& filename);

    void writeData(const SensorData& data);
};