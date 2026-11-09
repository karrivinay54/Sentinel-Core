
from pathlib import Path
import sys

import streamlit as st
import pandas as pd


# --------------------------------------------------
# Project paths and imports
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# --------------------------------------------------
# Latest integrated simulation run
# --------------------------------------------------


def get_latest_integrated_run():
    data_dir = PROJECT_ROOT / "cpp_engine" / "data"
    reports_dir = PROJECT_ROOT / "analytics" / "reports"

    simulation_files = sorted(
        data_dir.glob("sentinel_run_*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    for simulation_path in simulation_files:
        run_id = simulation_path.stem.replace(
            "sentinel_run_", "", 1
        )

        prediction_path = (
            reports_dir / f"sentinel_predictions_{run_id}.csv"
        )

        if not prediction_path.exists():
            continue

        try:
            simulation = pd.read_csv(simulation_path)
            predictions = pd.read_csv(prediction_path)

            required_simulation = {
                "Timestamp", "MachineID", "FaultType", "ActiveFault"
            }
            required_predictions = required_simulation | {
                "PredictedFault", "Confidence"
            }

            if not required_simulation.issubset(simulation.columns):
                continue
            if not required_predictions.issubset(predictions.columns):
                continue
            if simulation.empty or len(simulation) != len(predictions):
                continue

            keys = ["Timestamp", "MachineID"]
            if not simulation[keys].astype(str).equals(
                predictions[keys].astype(str)
            ):
                continue

            return simulation_path, prediction_path, run_id

        except (OSError, ValueError, pd.errors.ParserError):
            continue

    return None, None, None



LATEST_SIMULATION_PATH, LATEST_PREDICTIONS_PATH, LATEST_RUN_ID = (
    get_latest_integrated_run()
)

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

DATA_PATH = LATEST_SIMULATION_PATH

if DATA_PATH is not None and DATA_PATH.exists():
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
            "ActiveFault",
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
                    "ActiveFault",
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
        "No complete integrated simulation run found. Expected file: "
        f"{DATA_PATH}"
    )




# Integrated Digital Twin + ML Monitoring
# --------------------------------------------------

if LATEST_RUN_ID:
    st.caption(f"Displaying integrated simulation run: {LATEST_RUN_ID}")
else:
    st.warning(
        "No matching simulation and prediction files found. "
        "Run the Sentinel-Core pipeline first."
    )

st.divider()
st.header("Integrated Digital Twin Monitoring")

PREDICTIONS_PATH = LATEST_PREDICTIONS_PATH

if PREDICTIONS_PATH is None or not PREDICTIONS_PATH.exists():
    st.warning(
        "Inference results not found. Run analytics/scripts/run_inference.py first."
    )

else:
    try:
        predictions = pd.read_csv(PREDICTIONS_PATH)

        required_columns = [
            "Timestamp", "MachineID",
            "Temperature", "Vibration", "Current",
            "Voltage", "RPM", "DegradationLevel",
            "State", "FaultType", "ActiveFault", "PredictedFault",
            "Confidence",
            "Prob_BEARING_WEAR",
            "Prob_COOLING_FAILURE",
            "Prob_MISALIGNMENT",
            "Prob_NONE",
            "Prob_OVERLOAD",
        ]

        missing = [
            col for col in required_columns
            if col not in predictions.columns
        ]

        if missing:
            st.error(f"Missing columns: {missing}")

        elif predictions.empty:
            st.warning("The inference output contains no records.")

        else:
            predictions["Timestamp"] = pd.to_datetime(
                predictions["Timestamp"], errors="coerce"
            )

            predictions = predictions.dropna(
                subset=["Timestamp", "MachineID"]
            ).copy()

            predictions = predictions.sort_values("Timestamp")

            # Latest record for every machine
            latest_records = (
                predictions.groupby("MachineID", as_index=False)
                .tail(1)
                .sort_values("MachineID")
            )

            st.caption(
                "Integrated results from C++ Digital Twin simulation "
                "and Python Random Forest inference."
            )

            # System summary
            total_machines = latest_records["MachineID"].nunique()
            healthy_count = (
                latest_records["State"] == "HEALTHY"
            ).sum()
            warning_count = (
                latest_records["State"] == "WARNING"
            ).sum()
            fault_count = latest_records["State"].isin(
                ["FAULT", "CRITICAL"]
            ).sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Machines", total_machines)
            col2.metric("Healthy", int(healthy_count))
            col3.metric("Warning", int(warning_count))
            col4.metric("Fault / Critical", int(fault_count))

            st.divider()
            st.subheader("Machine Overview")

            overview_columns = [
                "MachineID",
                "State",
                "DegradationLevel",
                "PredictedFault",
                "Confidence",
                "FaultType",
                "ActiveFault",
                "Timestamp",
            ]

            overview = latest_records[overview_columns].copy()
            overview["Confidence"] = (
                overview["Confidence"] * 100
            ).round(2).astype(str) + "%"

            st.dataframe(
                overview,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()
            st.subheader("Individual Machine Analysis")

            machine_ids = latest_records["MachineID"].tolist()

            selected_machine = st.selectbox(
                "Select machine",
                machine_ids,
                key="integrated_machine",
            )

            machine_data = predictions[
                predictions["MachineID"] == selected_machine
            ].sort_values("Timestamp").copy()

            latest = machine_data.iloc[-1]

            # Current machine information
            st.markdown(f"### Machine {selected_machine}")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Machine State", str(latest["State"]))
            c2.metric(
                "Degradation",
                f"{latest['DegradationLevel']:.2f}",
            )
            c3.metric(
                "Predicted Fault",
                str(latest["PredictedFault"]),
            )
            c4.metric(
                "Confidence",
                f"{latest['Confidence']:.2%}",
            )

            st.write(
                f"**Original fault scenario:** {latest['FaultType']}"
            )
            st.write(
                f"**Currently active fault:** {latest['ActiveFault']}"
            )

            # Sensor measurements
            st.subheader("Latest Sensor Readings")

            sensor_cols = st.columns(5)

            sensor_values = [
                ("Temperature", f"{latest['Temperature']:.2f} °C"),
                ("Vibration", f"{latest['Vibration']:.4f} mm/s"),
                ("Current", f"{latest['Current']:.3f} A"),
                ("Voltage", f"{latest['Voltage']:.2f} V"),
                ("RPM", f"{latest['RPM']:.0f}"),
            ]

            for col, (label, value) in zip(
                sensor_cols, sensor_values
            ):
                col.metric(label, value)

            # Probability estimates
            st.subheader("Fault Probability Estimates")

            probability_columns = [
                "Prob_BEARING_WEAR",
                "Prob_COOLING_FAILURE",
                "Prob_MISALIGNMENT",
                "Prob_NONE",
                "Prob_OVERLOAD",
            ]

            probabilities = {
                col.replace("Prob_", ""): float(latest[col])
                for col in probability_columns
            }

            for fault, probability in sorted(
                probabilities.items(),
                key=lambda item: item[1],
                reverse=True,
            ):
                st.write(f"**{fault}** — {probability:.2%}")
                st.progress(
                    max(0.0, min(1.0, probability))
                )

            st.caption(
                "Probability values are Random Forest model estimates, "
                "not calibrated real-world fault probabilities."
            )

            # Sensor history
            st.subheader("Sensor and Degradation Trends")

            sensor_options = {
                "Temperature (°C)": "Temperature",
                "Vibration (mm/s)": "Vibration",
                "Current (A)": "Current",
                "Voltage (V)": "Voltage",
                "RPM": "RPM",
                "Degradation Level": "DegradationLevel",
            }

            selected_label = st.selectbox(
                "Select measurement",
                list(sensor_options.keys()),
                key="integrated_sensor",
            )

            selected_column = sensor_options[selected_label]

            trend_data = machine_data.set_index("Timestamp")[
                [selected_column]
            ]

            st.line_chart(
                trend_data,
                use_container_width=True,
            )

            # Recent history
            st.subheader("Recent Simulation Records")

            recent_columns = [
                "Timestamp", "Temperature", "Vibration",
                "Current", "Voltage", "RPM",
                "DegradationLevel", "State",
                "FaultType", "ActiveFault", "PredictedFault", "Confidence",
            ]

            st.dataframe(
                machine_data[recent_columns].tail(10),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "This view displays batch simulation and inference results. "
                "It does not represent live industrial telemetry."
            )

    except (OSError, ValueError, KeyError, TypeError) as error:
        st.error(f"Unable to load integrated monitoring data: {error}")




# --------------------------------------------------
# Machine Event History
# --------------------------------------------------

st.divider()
st.header("Machine Event History")

EVENT_DATA_PATH = LATEST_PREDICTIONS_PATH

if EVENT_DATA_PATH is not None and EVENT_DATA_PATH.exists():

    try:
        event_data = pd.read_csv(EVENT_DATA_PATH)

        required_event_columns = [
            "Timestamp",
            "MachineID",
            "State",
            "DegradationLevel",
            "FaultType",
            "ActiveFault",
            "PredictedFault",
            "Confidence",
        ]

        missing = [
            col for col in required_event_columns
            if col not in event_data.columns
        ]

        if missing:
            st.error(f"Missing event columns: {missing}")

        else:
            event_data["Timestamp"] = pd.to_datetime(
                event_data["Timestamp"],
                errors="coerce",
            )

            event_data = event_data.dropna(
                subset=["Timestamp", "MachineID", "State"]
            ).copy()

            event_data = event_data.sort_values(
                ["MachineID", "Timestamp"]
            )

            # Detect initial states and subsequent state transitions
            event_data["PreviousState"] = (
                event_data.groupby("MachineID")["State"].shift(1)
            )

            events = event_data[
                event_data["State"] != event_data["PreviousState"]
            ].copy()

            events["EventType"] = events["PreviousState"].apply(
                lambda state: (
                    "INITIAL STATE"
                    if pd.isna(state)
                    else "STATE TRANSITION"
                )
            )

            events["Transition"] = events.apply(
                lambda row: (
                    f"INITIAL → {row['State']}"
                    if pd.isna(row["PreviousState"])
                    else f"{row['PreviousState']} → {row['State']}"
                ),
                axis=1,
            )

            # Event summary
            total_events = len(events)
            actual_transitions = (
                events["EventType"] == "STATE TRANSITION"
            ).sum()

            affected_machines = events.loc[
                events["EventType"] == "STATE TRANSITION",
                "MachineID",
            ].nunique()

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric("Total Event Entries", total_events)
            metric2.metric("State Transitions", int(actual_transitions))
            metric3.metric("Machines with Transitions", affected_machines)

            st.divider()

            # Machine filter
            machine_options = ["All Machines"] + sorted(
                events["MachineID"].unique().tolist()
            )

            selected_event_machine = st.selectbox(
                "Filter events by machine",
                machine_options,
                key="event_machine_filter",
            )

            filtered_events = events.copy()

            if selected_event_machine != "All Machines":
                filtered_events = filtered_events[
                    filtered_events["MachineID"]
                    == selected_event_machine
                ]

            # Chronological event history
            st.subheader("Chronological Event Timeline")

            display_events = filtered_events.sort_values(
                "Timestamp",
                ascending=False,
            ).copy()

            display_events["Confidence"] = (
                display_events["Confidence"] * 100
            ).round(2).astype(str) + "%"

            event_columns = [
                "Timestamp",
                "MachineID",
                "EventType",
                "Transition",
                "DegradationLevel",
                "FaultType",
                "ActiveFault",
                "PredictedFault",
                "Confidence",
            ]

            st.dataframe(
                display_events[event_columns],
                use_container_width=True,
                hide_index=True,
            )

            # Lifecycle summary
            st.divider()
            st.subheader("Machine Lifecycle Summary")

            lifecycle_summary = (
                events.groupby("MachineID")
                .agg(
                    EventEntries=("State", "size"),
                    Transitions=("EventType", lambda x: (
                        x == "STATE TRANSITION"
                    ).sum()),
                    FinalState=("State", "last"),
                )
                .reset_index()
            )

            st.dataframe(
                lifecycle_summary,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Events are extracted from changes in the simulated "
                "machine State. The first record for each machine is "
                "shown as its initial state. ML predictions are displayed "
                "separately and do not determine the simulated state."
            )

    except (OSError, ValueError, KeyError, TypeError) as error:
        st.error(f"Unable to load machine event history: {error}")

else:
    st.warning(
        "Event history dataset not found. Expected file: "
        f"{EVENT_DATA_PATH}"
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Sentinel-Core | Software Simulation Prototype"
)
