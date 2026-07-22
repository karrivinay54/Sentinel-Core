#include "../include/SensorData.h"
#include "../include/CSVWriter.h"

#include <iostream>

int main()
{
    SensorData reading(
        "2026-07-22 16:35:01",
        "M001",
        36.8,
        0.32,
        3.05,
        229.6,
        1498
    );

    CSVWriter writer("cpp_engine/data/sensor_data.csv");

    writer.writeData(reading);

    std::cout << "Sensor data written successfully.\n";

    return 0;
}