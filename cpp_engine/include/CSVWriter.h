#pragma once

#include <string>
#include "DatasetRecord.h"

class CSVWriter
{
private:
    std::string filename;

public:
    explicit CSVWriter(const std::string& filename);

    void write(const DatasetRecord& record);
};