#include "../include/SimulationManager.h"

#include "../include/DatasetRecord.h"

#include <iostream>

SimulationManager::SimulationManager(const SimulationConfig& config)
    : config(config),
      twin(config.getMachineID()),
      writer(config.getOutputFile())
{
}

void SimulationManager::run()
{
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
}