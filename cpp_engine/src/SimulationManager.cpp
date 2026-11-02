#include "../include/SimulationManager.h"
#include "../include/DatasetRecord.h"

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>

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
        std::cout << "\n========== ITERATION "
                  << i + 1 << " ==========\n";

        for (auto& twin : twins)
        {
            twin.update();

            SensorData reading = twin.generateReading();

            DatasetRecord record(
                reading,
                twin.getDegradationLevel(),
                twin.getState(),
                twin.getAssignedFault()
            );

            reading.display();
            writer.write(record);

            std::cout << "-----------------------------\n";
        }

        // --------------------------------------------------------
        // OPERATOR MAINTENANCE CONTROL
        // --------------------------------------------------------

        std::cout << "\nMachines requiring maintenance:\n";

        bool criticalMachineFound = false;

        for (const auto& twin : twins)
        {
            if (twin.getState() == MachineState::CRITICAL)
            {
                criticalMachineFound = true;

                std::cout << twin.getMachineID() << " ";
            }
        }

        if (criticalMachineFound)
        {
            std::cout << "\nEnter machine ID to authorize maintenance "
                      << "(or press Enter to skip): ";

            std::string selectedMachine;
            std::getline(std::cin >> std::ws, selectedMachine);

            if (!selectedMachine.empty())
            {
                bool machineFound = false;

                for (auto& twin : twins)
                {
                    if (twin.getMachineID() == selectedMachine)
                    {
                        machineFound = true;

                        if (twin.requestMaintenance())
                        {
                            std::cout << "Maintenance authorized for "
                                      << selectedMachine << "\n";
                        }
                        else
                        {
                            std::cout << "Maintenance request rejected.\n";
                        }

                        break;
                    }
                }

                if (!machineFound)
                {
                    std::cout << "Machine ID not found.\n";
                }
            }
        }
    }

    std::cout << "\nSimulation completed successfully.\n";
}