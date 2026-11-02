#pragma once

#include <string>

enum class MachineState
{
    OFF,
    STARTING,
    HEALTHY,
    WARNING,
    FAULT,
    CRITICAL,
    MAINTENANCE,
    RECOVERY,
    SHUTDOWN
};

// Convert MachineState to readable text
inline std::string toString(MachineState state)
{
    switch (state)
    {
    case MachineState::OFF:
        return "OFF";

    case MachineState::STARTING:
        return "STARTING";

    case MachineState::HEALTHY:
        return "HEALTHY";

    case MachineState::WARNING:
        return "WARNING";

    case MachineState::FAULT:
        return "FAULT";

    case MachineState::CRITICAL:
        return "CRITICAL";

    case MachineState::MAINTENANCE:
        return "MAINTENANCE";

    case MachineState::RECOVERY:
        return "RECOVERY";

    case MachineState::SHUTDOWN:
        return "SHUTDOWN";

    default:
        return "UNKNOWN";
    }
}