#include "../include/SensorData.h"

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

    reading.display();

    std::cout << "\nCSV Output:\n";
    std::cout << reading.toCSV() << '\n';

    return 0;
}
