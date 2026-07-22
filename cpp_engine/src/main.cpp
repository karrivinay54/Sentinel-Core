#include "../include/MachineState.h"

#include <iostream>

int main()
{
    MachineState state = MachineState::HEALTHY;

    std::cout << "Current Machine State : "
              << toString(state)
              << '\n';

    return 0;
}