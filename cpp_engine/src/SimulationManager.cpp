#include "../include/SimulationManager.h"
#include "../include/DatasetRecord.h"

#include <iostream>
#include <iomanip>
#include <sstream>

SimulationManager::SimulationManager(const SimulationConfig& config)
    : config(config),
      writer(config.getOutputFile())
{
    for (int i = 1; i <= config.getMachineCount(); ++i)
    {
        std::ostringstream machineID;

        machineID << "M"
                  << std::setw(3)
                  << std::setfill('0')
                  << i;

        twins.emplace_back(
            machineID.str(),
            config.getFaultForMachine(i - 1)
        );
    }
}

void SimulationManager::run()
{
    for (int i = 0; i < config.getNumIterations(); ++i)
    {
        for (auto& twin : twins)
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
    }

    std::cout << "\nSimulation completed successfully.\n";
}