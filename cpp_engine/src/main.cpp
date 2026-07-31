#include "../include/CSVWriter.h"
#include "../include/DigitalTwin.h"
#include "../include/SimulationConfig.h"

#include <iostream>
#include <cstdio>

int main()
{
    std::remove("cpp_engine/data/sensor_data.csv");

    SimulationConfig config(
        "M001",
        "cpp_engine/data/sensor_data.csv",
        50
    );

    DigitalTwin twin(config.getMachineID());

    CSVWriter writer(config.getOutputFile());

    for (int i = 0; i < config.getNumIterations(); i++)
    {
        twin.update();

        SensorData reading = twin.generateReading();

        DatasetRecord record(
            reading,
            twin.getState(),
            twin.getFaultType()
        );

        reading.display();

        writer.write(record);

        std::cout << "-----------------------------\n";
    }

    std::cout << "\nSimulation completed successfully.\n";

    return 0;
}