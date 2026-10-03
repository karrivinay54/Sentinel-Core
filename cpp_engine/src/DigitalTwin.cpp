#include "../include/DigitalTwin.h"

#include <cmath>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>


// ================================================================
// CONSTRUCTOR
// ================================================================

DigitalTwin::DigitalTwin(
    const std::string& machineID,
    FaultType fault
)
    : machineID(machineID),
      state(MachineState::HEALTHY),
      assignedFault(fault),
      currentFault(FaultType::NONE),

      // ------------------------------------------------------------
      // Initial sensor values
      // ------------------------------------------------------------

      temperature(36.8),
      vibration(0.32),
      current(3.05),
      voltage(229.6),
      rpm(1498),

      // ------------------------------------------------------------
      // Simulation variables
      // ------------------------------------------------------------

      runningTime(0),
      degradationLevel(0.0),

      simulationStartTime(std::time(nullptr)),

      // Random seed
      generator(std::random_device{}()),

      // ------------------------------------------------------------
      // Machine-specific baseline
      //
      // These are initialized below because they require
      // random distributions.
      // ------------------------------------------------------------

      baselineTemperature(HEALTHY_TEMPERATURE),
      baselineVibration(HEALTHY_VIBRATION),
      baselineCurrent(HEALTHY_CURRENT),
      baselineVoltage(HEALTHY_VOLTAGE),
      baselineRPM(HEALTHY_RPM),

      // ------------------------------------------------------------
      // Fault effects
      // ------------------------------------------------------------

      temperatureEffect(0.0),
      vibrationEffect(0.0),
      currentEffect(0.0),
      voltageEffect(0.0),
      rpmEffect(0),

      // ------------------------------------------------------------
      // Initial operating targets
      // ------------------------------------------------------------

      targetTemperature(HEALTHY_TEMPERATURE),
      targetVibration(HEALTHY_VIBRATION),
      targetCurrent(HEALTHY_CURRENT),
      targetVoltage(HEALTHY_VOLTAGE),
      targetRPM(HEALTHY_RPM)
{
    // ============================================================
    // GENERATE MACHINE-SPECIFIC BASELINE
    //
    // These variations are generated ONCE for each machine.
    // They remain fixed during the entire simulation.
    //
    // This means:
    //
    // M001 may naturally run slightly warmer.
    // M002 may naturally have slightly higher vibration.
    // M003 may naturally draw slightly different current.
    //
    // But these differences do not randomly change every timestep.
    // ============================================================

    std::uniform_real_distribution<double> temperatureVariation(
        -0.5,
        0.5
    );

    std::uniform_real_distribution<double> vibrationVariation(
        -0.04,
        0.04
    );

    std::uniform_real_distribution<double> currentVariation(
        -0.10,
        0.10
    );

    std::uniform_real_distribution<double> voltageVariation(
        -1.0,
        1.0
    );

    std::uniform_int_distribution<int> rpmVariation(
        -8,
        8
    );


    baselineTemperature =
        HEALTHY_TEMPERATURE + temperatureVariation(generator);

    baselineVibration =
        HEALTHY_VIBRATION + vibrationVariation(generator);

    baselineCurrent =
        HEALTHY_CURRENT + currentVariation(generator);

    baselineVoltage =
        HEALTHY_VOLTAGE + voltageVariation(generator);

    baselineRPM =
        HEALTHY_RPM + rpmVariation(generator);


    // ============================================================
    // INITIAL SENSOR VALUES FOLLOW THE MACHINE BASELINE
    // ============================================================

    temperature = baselineTemperature;
    vibration   = baselineVibration;
    current     = baselineCurrent;
    voltage     = baselineVoltage;
    rpm         = baselineRPM;


    // ============================================================
    // INITIAL TARGETS FOLLOW THE MACHINE BASELINE
    // ============================================================

    targetTemperature = baselineTemperature;
    targetVibration   = baselineVibration;
    targetCurrent     = baselineCurrent;
    targetVoltage     = baselineVoltage;
    targetRPM         = baselineRPM;
}


// ================================================================
// UPDATE
// ================================================================

void DigitalTwin::update()
{
    runningTime++;

    // Step 1: Increase degradation
    updateDegradation();

    // Step 2: Determine machine state
    updateState();

    // Step 3: Determine currently reported fault
    updateFault();

    // Step 4: Determine physical effect of assigned fault
    updateFaultEffects();

    // Step 5: Calculate sensor targets
    updateTargets();

    // Step 6: Move sensors toward targets and add noise
    updateSensors();
}


// ================================================================
// UPDATE MACHINE STATE
// ================================================================

void DigitalTwin::updateState()
{
    if (degradationLevel < 0.40)
    {
        state = MachineState::HEALTHY;
    }
    else if (degradationLevel < 0.70)
    {
        state = MachineState::WARNING;
    }
    else if (degradationLevel < 0.90)
    {
        state = MachineState::FAULT;
    }
    else
    {
        state = MachineState::CRITICAL;
    }


    // ------------------------------------------------------------
    // Console output
    // ------------------------------------------------------------

    std::cout << "[STATE] ";

    switch (state)
    {
        case MachineState::HEALTHY:

            std::cout << "HEALTHY";
            break;

        case MachineState::WARNING:

            std::cout << "WARNING";
            break;

        case MachineState::FAULT:

            std::cout << "FAULT";
            break;

        case MachineState::CRITICAL:

            std::cout << "CRITICAL";
            break;

        default:

            std::cout << "UNKNOWN";
            break;
    }

    std::cout << "\n";
}


// ================================================================
// UPDATE DEGRADATION
// ================================================================

void DigitalTwin::updateDegradation()
{
    const double DEGRADATION_RATE = 0.02;

    degradationLevel += DEGRADATION_RATE;

    if (degradationLevel > 1.0)
    {
        degradationLevel = 1.0;
    }


    std::cout << "[DEGRADATION] Level: "
              << degradationLevel
              << "\n";
}


// ================================================================
// UPDATE CURRENT FAULT LABEL
// ================================================================
//
// IMPORTANT:
//
// assignedFault
//      = fault scenario assigned to the machine
//
// currentFault
//      = fault currently reported by the state logic
//
// We are preserving your existing logic here.
//
// HEALTHY:
//      currentFault = NONE
//
// WARNING / FAULT / CRITICAL:
//      currentFault = assignedFault
//
// The sensor physics itself is handled separately by
// updateFaultEffects() and uses assignedFault.
// ================================================================

void DigitalTwin::updateFault()
{
    if (state == MachineState::HEALTHY)
    {
        currentFault = FaultType::NONE;
    }
    else
    {
        currentFault = assignedFault;
    }
}


// ================================================================
// UPDATE FAULT EFFECTS
// ================================================================
//
// These values represent the maximum sensor change when:
//
//     degradationLevel = 1.0
//
// The actual sensor target is calculated later as:
//
//     baseline + degradation × effect
//
// This separates:
//     1. Machine variation
//     2. Fault signature
//     3. Sensor noise
//
// which is the design we established for Sentinel-Core.
// ================================================================

void DigitalTwin::updateFaultEffects()
{
    // ------------------------------------------------------------
    // Reset effects first
    // ------------------------------------------------------------

    temperatureEffect = 0.0;
    vibrationEffect   = 0.0;
    currentEffect     = 0.0;
    voltageEffect     = 0.0;
    rpmEffect         = 0;


    // ------------------------------------------------------------
    // Select effect according to the ASSIGNED fault scenario
    // ------------------------------------------------------------

    switch (assignedFault)
    {
        // ========================================================
        // NO FAULT
        // ========================================================

        case FaultType::NONE:

            temperatureEffect = 0.0;
            vibrationEffect   = 0.0;
            currentEffect     = 0.0;
            voltageEffect     = 0.0;
            rpmEffect         = 0;

            break;


        // ========================================================
        // BEARING WEAR
        //
        // Dominant signature:
        //      Increased vibration
        //
        // Secondary:
        //      Slight temperature/current increase
        //      Slight RPM reduction
        // ========================================================

        case FaultType::BEARING_WEAR:

            temperatureEffect = +1.5;
            vibrationEffect   = +0.20;
            currentEffect     = +0.20;
            voltageEffect     = 0.0;
            rpmEffect         = -10;

            break;


        // ========================================================
        // MISALIGNMENT
        //
        // Dominant signature:
        //      Strong vibration
        //
        // Secondary:
        //      Slight temperature/current increase
        //      RPM reduction
        // ========================================================

        case FaultType::MISALIGNMENT:

            temperatureEffect = +1.8;
            vibrationEffect   = +0.35;
            currentEffect     = +0.25;
            voltageEffect     = 0.0;
            rpmEffect         = -12;

            break;


        // ========================================================
        // COOLING FAILURE
        //
        // Dominant signature:
        //      Strong temperature increase
        //
        // Other sensors remain relatively stable.
        // ========================================================

        case FaultType::COOLING_FAILURE:

            temperatureEffect = +6.0;
            vibrationEffect   = 0.0;
            currentEffect     = +0.15;
            voltageEffect     = 0.0;
            rpmEffect         = 0;

            break;


        // ========================================================
        // OVERLOAD
        //
        // Dominant signature:
        //      Strong current increase
        //
        // Secondary:
        //      Temperature increase
        //      Vibration increase
        //      Voltage drop
        //      RPM reduction
        // ========================================================

        case FaultType::OVERLOAD:

            temperatureEffect = +2.5;
            vibrationEffect   = +0.10;
            currentEffect     = +1.20;
            voltageEffect     = -4.0;
            rpmEffect         = -35;

            break;


        // ========================================================
        // DEFAULT
        // ========================================================

        default:

            temperatureEffect = 0.0;
            vibrationEffect   = 0.0;
            currentEffect     = 0.0;
            voltageEffect     = 0.0;
            rpmEffect         = 0;

            break;
    }
}


// ================================================================
// UPDATE SENSOR TARGETS
// ================================================================
//
// Core Sentinel-Core sensor model:
//
//     Target Sensor
//     = Machine Baseline
//     + Fault Effect × Degradation
//
// Example:
//
//     baseline temperature = 37.1 °C
//     fault effect         = +6.0 °C
//     degradation          = 0.50
//
//     target = 37.1 + (6.0 × 0.50)
//            = 40.1 °C
//
// The actual sensor reading then approaches this target gradually
// in updateSensors().
// ================================================================

void DigitalTwin::updateTargets()
{
    targetTemperature =
        baselineTemperature +
        degradationLevel * temperatureEffect;


    targetVibration =
        baselineVibration +
        degradationLevel * vibrationEffect;


    targetCurrent =
        baselineCurrent +
        degradationLevel * currentEffect;


    targetVoltage =
        baselineVoltage +
        degradationLevel * voltageEffect;


    targetRPM =
        baselineRPM +
        static_cast<int>(
            std::round(
                degradationLevel * rpmEffect
            )
        );
}


// ================================================================
// UPDATE SENSORS
// ================================================================
//
// Sensors do not instantly jump to their targets.
//
// Instead:
//
//     New Sensor
//     = Previous Sensor
//     + Noise
//     + Recovery toward target
//
// This preserves the gradual behavior already present in
// your original DigitalTwin implementation.
// ================================================================

void DigitalTwin::updateSensors()
{
    // ------------------------------------------------------------
    // Measurement noise
    //
    // These values are intentionally kept close to your existing
    // noise model for this step.
    // ------------------------------------------------------------

    std::uniform_real_distribution<double> tempNoise(
        -0.05,
        0.05
    );

    std::uniform_real_distribution<double> vibrationNoise(
        -0.01,
        0.01
    );

    std::uniform_real_distribution<double> currentNoise(
        -0.02,
        0.02
    );

    std::uniform_real_distribution<double> voltageNoise(
        -0.20,
        0.20
    );

    std::uniform_int_distribution<int> rpmNoise(
        -1,
        1
    );


    // ------------------------------------------------------------
    // Temperature
    // ------------------------------------------------------------

    temperature +=
        tempNoise(generator)
        +
        RECOVERY_FACTOR *
        (targetTemperature - temperature);


    // ------------------------------------------------------------
    // Vibration
    // ------------------------------------------------------------

    vibration +=
        vibrationNoise(generator)
        +
        RECOVERY_FACTOR *
        (targetVibration - vibration);


    // ------------------------------------------------------------
    // Current
    // ------------------------------------------------------------

    current +=
        currentNoise(generator)
        +
        RECOVERY_FACTOR *
        (targetCurrent - current);


    // ------------------------------------------------------------
    // Voltage
    // ------------------------------------------------------------

    voltage +=
        voltageNoise(generator)
        +
        RECOVERY_FACTOR *
        (targetVoltage - voltage);


    // ------------------------------------------------------------
    // RPM
    // ------------------------------------------------------------

    rpm +=
        rpmNoise(generator)
        +
        static_cast<int>(
            std::round(
                0.10 *
                (targetRPM - rpm)
            )
        );
}


// ================================================================
// GENERATE SENSOR READING
// ================================================================

SensorData DigitalTwin::generateReading()
{
    // Simulated timestamp advances with runningTime
    std::time_t simulatedTime =
        simulationStartTime + runningTime;


    std::tm* localTime =
        std::localtime(&simulatedTime);


    std::ostringstream timestamp;


    timestamp
        << std::put_time(
            localTime,
            "%Y-%m-%d %H:%M:%S"
        );


    return SensorData(
        timestamp.str(),
        machineID,
        temperature,
        vibration,
        current,
        voltage,
        rpm
    );
}


// ================================================================
// GET MACHINE STATE
// ================================================================

MachineState DigitalTwin::getState() const
{
    return state;
}


// ================================================================
// GET CURRENT FAULT
// ================================================================

FaultType DigitalTwin::getFaultType() const
{
    return currentFault;
}

FaultType DigitalTwin::getAssignedFault() const
{
    return assignedFault;
}


// ================================================================
// GET DEGRADATION LEVEL
// ================================================================

double DigitalTwin::getDegradationLevel() const
{
    return degradationLevel;
}