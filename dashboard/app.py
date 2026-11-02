
from pathlib import Path
import sys

import streamlit as st
import pandas as pd


# --------------------------------------------------
# Project paths and imports
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ANALYTICS_SCRIPTS = PROJECT_ROOT / "analytics" / "scripts"

if str(ANALYTICS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ANALYTICS_SCRIPTS))

from predict_fault import predict_fault


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Sentinel-Core | Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Dashboard header
# --------------------------------------------------

st.title("⚙️ Sentinel-Core")
st.subheader("Predictive Maintenance of Industrial Machines")

st.markdown(
    """
    **Observe · Interpret · Understand · Prevent**

    An intelligent machine-monitoring interface powered by
    a Digital Twin simulation and a Machine Learning classifier.
    """
)

st.divider()


# --------------------------------------------------
# System overview
# --------------------------------------------------

st.header("System Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Simulation Engine", "C++ Digital Twin")

with col2:
    st.metric("Fault Classifier", "Random Forest")

with col3:
    st.metric("Supported Fault Classes", "5")


st.divider()


# --------------------------------------------------
# Sensor input panel
# --------------------------------------------------

st.header("Machine Sensor Readings")

st.write(
    "Enter the sensor measurements to estimate the machine's "
    "most likely fault condition."
)

with st.form("sensor_input_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=200.0,
            value=38.2,
            step=0.0001,
            format="%.4f",
        )

        vibration = st.number_input(
            "Vibration (mm/s)",
            min_value=0.0,
            max_value=100.0,
            value=0.48,
            step=0.000001,
            format="%.6f",
        )

    with col2:
        current = st.number_input(
            "Current (A)",
            min_value=0.0,
            max_value=1000.0,
            value=3.25,
            step=0.00001,
            format="%.5f",
        )

        voltage = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            max_value=1000.0,
            value=228.7,
            step=0.0001,
            format="%.4f",
        )

    with col3:
        rpm = st.number_input(
            "Rotational Speed (RPM)",
            min_value=0.0,
            max_value=100000.0,
            value=1480.0,
            step=1.0,
            format="%.0f",
        )

    submitted = st.form_submit_button(
        "Analyze Machine",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Fault prediction
# --------------------------------------------------

if submitted:

    sensor_readings = {
        "Temperature": temperature,
        "Vibration": vibration,
        "Current": current,
        "Voltage": voltage,
        "RPM": rpm,
    }

    try:
        result = predict_fault(sensor_readings)

        st.divider()
        st.header("Fault Prediction Results")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                "Predicted Fault",
                result["predicted_fault"],
            )

        with result_col2:
            st.metric(
                "Model Probability Estimate",
                f"{result['confidence']:.2%}",
            )

            
        # --------------------------------------------------
        # Fault interpretation
        # --------------------------------------------------

        fault_guidance = {
            "BEARING_WEAR": {
                "title": "Possible bearing wear",
                "description": (
                    "The model identifies bearing wear as the "
                    "most likely class for these sensor readings."
                ),
                "action": (
                    "Review vibration and temperature trends, "
                    "inspect bearing condition, and compare readings "
                    "with the machine manufacturer's limits."
                ),
            },
            "COOLING_FAILURE": {
                "title": "Possible cooling failure",
                "description": (
                    "The model identifies cooling failure as the "
                    "most likely class for these sensor readings."
                ),
                "action": (
                    "Check cooling airflow, fans, coolant flow, "
                    "and temperature trends."
                ),
            },
            "MISALIGNMENT": {
                "title": "Possible shaft misalignment",
                "description": (
                    "The model identifies misalignment as the "
                    "most likely class for these sensor readings."
                ),
                "action": (
                    "Review vibration trends and arrange an "
                    "alignment inspection if warranted."
                ),
            },
            "NONE": {
                "title": "No fault class detected",
                "description": (
                    "The model predicts the NONE class for these "
                    "sensor readings. This does not establish that "
                    "the machine is healthy."
                ),
                "action": (
                    "Continue routine monitoring and compare all "
                    "readings with established operating limits."
                ),
            },
            "OVERLOAD": {
                "title": "Possible machine overload",
                "description": (
                    "The model identifies overload as the "
                    "most likely class for these sensor readings."
                ),
                "action": (
                    "Review current draw, load conditions, and "
                    "manufacturer-rated operating limits."
                ),
            },
        }

        predicted_fault = result["predicted_fault"]
        guidance = fault_guidance.get(predicted_fault)

        st.subheader("Fault Interpretation")

        if guidance:
            st.markdown(f"**{guidance['title']}**")
            st.write(guidance["description"])

            st.markdown("**Suggested checks**")
            st.write(guidance["action"])

        st.caption(
            "Guidance is indicative, not a confirmed diagnosis. "
            "Verify suspected faults using appropriate inspections "
            "and real machine measurements."
        )



        st.subheader("Class Probability Estimates")

        probabilities = result["probabilities"]

        for fault, probability in sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            st.write(f"**{fault}** — {probability:.2%}")
            st.progress(probability)

        st.caption(
            "These are model probability estimates, not guarantees "
            "of actual machine condition. This model has been "
            "evaluated using simulated data."
        )

    except (ValueError, TypeError) as error:
        st.error(f"Unable to analyze sensor readings: {error}")



# --------------------------------------------------
# Historical Sensor Monitoring
# --------------------------------------------------

st.divider()
st.header("Historical Sensor Monitoring")

DATA_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data_v5.csv"

if DATA_PATH.exists():
    try:
        history = pd.read_csv(DATA_PATH)

        required_columns = [
            "Timestamp",
            "MachineID",
            "Temperature",
            "Vibration",
            "Current",
            "Voltage",
            "RPM",
            "DegradationLevel",
            "State",
            "FaultType",
        ]

        missing_columns = [
            column for column in required_columns
            if column not in history.columns
        ]

        if missing_columns:
            st.error(
                f"Dataset is missing columns: {missing_columns}"
            )
        else:
            history["Timestamp"] = pd.to_datetime(
                history["Timestamp"], errors="coerce"
            )
            history = history.dropna(
                subset=["Timestamp", "MachineID"]
            )

            machines = sorted(
                history["MachineID"].unique().tolist()
            )

            selected_machine = st.selectbox(
                "Select a machine",
                machines,
                key="history_machine",
            )

            machine_history = history[
                history["MachineID"] == selected_machine
            ].copy()

            machine_history = machine_history.sort_values(
                "Timestamp"
            ).reset_index(drop=True)

            if not machine_history.empty:
                fault_classes = machine_history["FaultType"].unique()
                states = machine_history["State"].unique()

                info1, info2, info3 = st.columns(3)

                with info1:
                    st.metric(
                        "Recorded Readings",
                        len(machine_history),
                    )

                with info2:
                    st.metric(
                        "Fault Class",
                        ", ".join(map(str, fault_classes)),
                    )

                with info3:
                    st.metric(
                        "Latest Simulated State",
                        str(machine_history.iloc[-1]["State"]),
                    )

                st.subheader("Sensor Trends")

                sensor_options = {
                    "Temperature (°C)": "Temperature",
                    "Vibration (mm/s)": "Vibration",
                    "Current (A)": "Current",
                    "Voltage (V)": "Voltage",
                    "Rotational Speed (RPM)": "RPM",
                    "Degradation Level": "DegradationLevel",
                }

                selected_sensor_label = st.selectbox(
                    "Select a measurement",
                    list(sensor_options.keys()),
                    key="history_sensor",
                )

                selected_sensor = sensor_options[
                    selected_sensor_label
                ]

                chart_data = machine_history.set_index("Timestamp")[
                    [selected_sensor]
                ]

                st.line_chart(
                    chart_data,
                    y=selected_sensor,
                    use_container_width=True,
                )

                st.subheader("Recent Readings")

                display_columns = [
                    "Timestamp",
                    "Temperature",
                    "Vibration",
                    "Current",
                    "Voltage",
                    "RPM",
                    "DegradationLevel",
                    "State",
                    "FaultType",
                ]

                st.dataframe(
                    machine_history[display_columns].tail(10),
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    "This view displays recorded Digital Twin simulation "
                    "data, not live industrial sensor telemetry."
                )

    except (OSError, ValueError, KeyError) as error:
        st.error(f"Unable to load historical data: {error}")
else:
    st.warning(
        "V5 dataset not found. Expected file: "
        f"{DATA_PATH}"
    )



# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Sentinel-Core | Software Simulation Prototype"
)
