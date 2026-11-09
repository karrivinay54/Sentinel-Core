# Sentinel-Core
### Digital Twin-Based Framework for Multi-Sensor Machine Fault Monitoring and Predictive Maintenance

**Observe · Interpret · Understand · Prevent**

Sentinel-Core is a software simulation prototype that combines a C++ Digital Twin with a Python-based Machine Learning classifier to simulate industrial machine conditions, monitor sensor measurements, identify potential fault classes, and visualize machine behaviour through an interactive dashboard.

## 1. Project Overview

Sentinel-Core integrates three main components:

- **Digital Twin:** A C++17 simulation engine that generates multi-sensor machine data and simulates degradation, fault conditions, maintenance, and recovery.
- **Machine Learning:** A Random Forest classifier that estimates machine fault classes from sensor measurements.
- **Monitoring Dashboard:** A Streamlit application that displays historical sensor readings, machine states, fault predictions, sensor trends, and machine event history.

The project uses five simulated machines, each representing a different operating scenario.

## 2. System Architecture

```text
             SENTINEL-CORE
                    |
          C++ DIGITAL TWIN
                    |
          Multi-Sensor Data
                    |
              CSV Dataset
                    |
           PYTHON ML ENGINE
                    |
          Random Forest Model
                    |
          Fault Predictions
                    |
             Streamlit
               Dashboard
                    |
          Machine Monitoring
```

### Main Components

| Component | Technology | Responsibility |
|---|---|---|
| Simulation engine | C++17 | Machine and sensor simulation |
| Data storage | CSV | Sensor and simulation records |
| Fault classifier | Scikit-learn | Fault classification |
| Inference engine | Python | Batch predictions |
| Automation | PowerShell | Pipeline orchestration |
| Dashboard | Streamlit | Monitoring and visualization |

## 3. Simulated Machine Scenarios

The Digital Twin simulates five machines:

| Machine ID | Original Fault Scenario |
|---|---|
| M001 | NONE |
| M002 | BEARING_WEAR |
| M003 | MISALIGNMENT |
| M004 | COOLING_FAILURE |
| M005 | OVERLOAD |

### Simulated Sensor Parameters

- Temperature (°C)
- Vibration (mm/s)
- Current (A)
- Voltage (V)
- Rotational Speed (RPM)

The simulation also tracks degradation levels, operating states, maintenance events, and recovery behaviour.

### Machine States

| State | Degradation Level |
|---|---|
| HEALTHY | Below 0.40 |
| WARNING | 0.40 to below 0.70 |
| FAULT | 0.70 to below 0.90 |
| CRITICAL | 0.90 and above |

MAINTENANCE and RECOVERY are additional lifecycle states.

## 4. Machine Learning Model

The integrated classifier uses a Random Forest model trained on simulated sensor measurements.

**Model:** `sentinel_fault_classifier_v5.pkl`

**Training dataset:** `sensor_data_v5.csv`

**Input features:**
1. Temperature
2. Vibration
3. Current
4. Voltage
5. RPM

**Target:** `FaultType`

**Model configuration:**
- 200 estimators
- Maximum depth: 8
- Random state: 42

The classifier supports five fault classes:

- NONE
- BEARING_WEAR
- MISALIGNMENT
- COOLING_FAILURE
- OVERLOAD

The model generates predicted fault labels, confidence estimates, and class probability estimates.

**Important:** The model uses synthetic simulation data. Its predictions are experimental estimates and should not be interpreted as validated real-world industrial fault detection.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| C++17 | Digital Twin simulation |
| Python 3.8.3 | ML and application execution environment tested |
| NumPy | Numerical operations |
| Pandas | Dataset processing |
| Scikit-learn | Random Forest classifier |
| Joblib | Model serialization |
| Streamlit | Interactive dashboard |
| CMake | C++ build system |
| PowerShell | Pipeline automation |

## 6. Repository Structure

```text
Sentinel-Core/
│
├── analytics/
│   ├── models/
│   │   └── sentinel_fault_classifier_v5.pkl
│   │
│   ├── reports/
│   │
│   └── scripts/
│       ├── predict_fault.py
│       ├── run_inference.py
│       ├── train_fault_classifier_v5.py
│       └── ...
│
├── cpp_engine/
│   ├── data/
│   │   └── sensor_data_v5.csv
│   ├── include/
│   ├── src/
│   └── CMakeLists.txt
│
├── dashboard/
│   └── app.py
│
├── datasets/
│   └── paderborn/
│       └── processed/
│
├── docs/
├── tests/
├── requirements.txt
├── run_sentinel.ps1
└── README.md
```

## 7. Installation and Setup

### Prerequisites

- Windows operating system
- Python 3.8.3 or a compatible tested environment
- C++17-compatible compiler
- CMake
- Git

### Clone the Repository

```powershell
git clone https://github.com/karrivinay54/Sentinel-Core.git

cd Sentinel-Core
```

### Install Python Dependencies

```powershell
python -m pip install -r requirements.txt
```

Dependencies are listed in `requirements.txt`.

### Build and Run the Complete Pipeline

Run the master PowerShell script from the project root:

```powershell
.\run_sentinel.ps1
```

The script performs four stages:

1. Builds the C++ Digital Twin using CMake.
2. Runs the machine simulation.
3. Executes Python batch inference.
4. Validates the generated sensor and prediction datasets.

Each execution generates timestamped simulation and prediction files.

## 8. Launch the Dashboard

After successfully running the simulation pipeline:

```powershell
streamlit run .\dashboard\app.py
```

The dashboard provides:

- Manual sensor input and fault estimation.
- Historical sensor monitoring.
- Integrated Digital Twin and ML monitoring.
- Machine-level analysis.
- Sensor and degradation trends.
- Fault probability estimates.
- Recent simulation records.
- Machine event history and lifecycle summaries.

The dashboard reads the latest matching simulation and inference outputs.

## 9. Additional Research: Paderborn Bearing Dataset

The project also includes a separate experimental investigation using the Paderborn University bearing dataset.

This experiment explores vibration-based bearing fault classification using real experimental data.

It is a separate research component and is not currently integrated into the main five-class Sentinel-Core inference pipeline.

## 10. Project Limitations

- The main Digital Twin operates using simulated sensor measurements.
- The classifier is trained on synthetic data.
- Model confidence estimates are not necessarily calibrated probabilities.
- The system does not currently provide validated Remaining Useful Life (RUL) predictions.
- Real industrial sensor integration and hardware deployment remain future development areas.
- The Paderborn experiment is independent of the main integrated model.

## 11. Future Scope

- Integrate physical sensors using embedded hardware.
- Develop real-time sensor acquisition.
- Improve fault classification using real industrial datasets.
- Explore temporal fault prediction.
- Investigate Remaining Useful Life estimation.
- Deploy the monitoring framework on edge devices such as Raspberry Pi.
- Extend the Digital Twin with more realistic machine behaviour.

## 12. Project Philosophy

**Observe · Interpret · Understand · Prevent**

Sentinel-Core aims to demonstrate how Digital Twin simulation, multi-sensor monitoring, and Machine Learning can work together as a foundation for intelligent predictive maintenance.

---

**Sentinel-Core | Software Simulation Prototype**

GitHub: https://github.com/karrivinay54/Sentinel-Core
