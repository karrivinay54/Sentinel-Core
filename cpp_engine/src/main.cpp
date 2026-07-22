#include "../include/CSVWriter.h"
#include "../include/DigitalTwin.h"

#include <iostream>

int main()
{
    DigitalTwin twin("M001");

    SensorData reading = twin.generateReading();

    reading.display();

    CSVWriter writer("cpp_engine/data/sensor_data.csv");

    writer.writeData(reading);

    std::cout << "\nSensor data saved.\n";

    return 0;
}