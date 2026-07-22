#include "../include/CSVWriter.h"
#include "../include/DigitalTwin.h"

#include <iostream>
#include <cstdio>

int main()
{
    std::remove("cpp_engine/data/sensor_data.csv");

    DigitalTwin twin("M001");

    CSVWriter writer("cpp_engine/data/sensor_data.csv");

    for (int i = 0; i < 20; i++)
    {
        twin.update();

        SensorData reading = twin.generateReading();

        reading.display();

        writer.writeData(reading);

        std::cout << "-----------------------------\n";
    }

    std::cout << "\nSimulation completed successfully.\n";

    return 0;
}