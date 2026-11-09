#pragma once

#include <random>
#include <string>
#include <ctime>

#include "MachineState.h"
#include "SensorData.h"
#include "FaultType.h"

class DigitalTwin
{
private:

    // ============================================================
    // MACHINE IDENTITY
    // ============================================================

    std::string machineID;

    // Current machine operating state
    MachineState state;

    // Original fault scenario assigned at machine creation.
    // Never changes during the simulation.
    FaultType originalFault;

    // Current fault scenario used by the simulation.
    // Can be cleared after maintenance.
    FaultType assignedFault;

    // Fault currently reported by the machine state logic.
    FaultType currentFault;

    // ============================================================
    // CURRENT SENSOR VALUES
    // ============================================================

    double temperature;
    double vibration;
    double current;
    double voltage;
    int rpm;


    // ============================================================
    // SIMULATION VARIABLES
    // ============================================================

    int runningTime;

    // 0.0 = healthy
    // 1.0 = maximum simulated degradation
    double degradationLevel;
    // Maintenance and recovery tracking
    bool maintenanceRequested;
    int maintenanceDuration;
    int recoveryDuration;
    int maintenanceElapsed;
    int recoveryElapsed;

    // Used to generate simulated timestamps
    std::time_t simulationStartTime;

    // Random number generator
    std::mt19937 generator;


    // ============================================================
    // HEALTHY NOMINAL OPERATING POINTS
    // ============================================================

    static constexpr double HEALTHY_TEMPERATURE = 36.8;
    static constexpr double HEALTHY_VIBRATION   = 0.32;
    static constexpr double HEALTHY_CURRENT     = 3.05;
    static constexpr double HEALTHY_VOLTAGE     = 229.6;
    static constexpr int    HEALTHY_RPM         = 1498;


    // ============================================================
    // MACHINE-SPECIFIC HEALTHY BASELINE
    //
    // Every machine is slightly different.
    // These values are generated once when the machine is created
    // and remain persistent throughout the simulation.
    // ============================================================

    double baselineTemperature;
    double baselineVibration;
    double baselineCurrent;
    double baselineVoltage;
    int baselineRPM;


    // ============================================================
    // FAULT-SPECIFIC SENSOR EFFECTS
    //
    // These represent the sensor change at degradationLevel = 1.0.
    //
    // Actual effect during simulation:
    //
    //     Fault Effect × degradationLevel
    //
    // Therefore the fault develops gradually.
    // ============================================================

    double temperatureEffect;
    double vibrationEffect;
    double currentEffect;
    double voltageEffect;
    int rpmEffect;


    // ============================================================
    // SENSOR RECOVERY / MEAN REVERSION
    // ============================================================

    static constexpr double RECOVERY_FACTOR = 0.05;


    // ============================================================
    // CURRENT OPERATING TARGETS
    //
    // Sensors gradually move toward these targets.
    // ============================================================

    double targetTemperature;
    double targetVibration;
    double targetCurrent;
    double targetVoltage;
    int targetRPM;


    // ============================================================
    // INTERNAL FUNCTIONS
    // ============================================================

    void updateState();

    void updateFault();

    void updateDegradation();

    // Determines the effect of the assigned fault
    void updateFaultEffects();

    // Calculates the current sensor targets
    void updateTargets();

    // Adds noise and moves sensors toward their targets
    void updateSensors();
    // Maintenance lifecycle
    void updateMaintenance();
    void updateRecovery();
    void restoreHealthyBaseline();


public:

    // ============================================================
    // CONSTRUCTOR
    // ============================================================

    DigitalTwin(
        const std::string& machineID,
        FaultType fault
    );


    // ============================================================
    // SIMULATION UPDATE
    // ============================================================

    void update();

    // Operator-authorized maintenance command
    bool requestMaintenance();

    // Machine identity
    std::string getMachineID() const;

    // Maintenance status
    bool isMaintenanceRequested() const;


    // ============================================================
    // DATA GENERATION
    // ============================================================

    SensorData generateReading();


        // ============================================================
    // GETTERS
    // ============================================================

    MachineState getState() const;

    FaultType getFaultType() const;
    FaultType getAssignedFault() const;
    FaultType getOriginalFault() const;

    double getDegradationLevel() const;

};
