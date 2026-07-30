import streamlit as st

from simulator.sensor_simulator import (
    generate_environment,
    calculate_sensor_scores
)

from ai.predict import predict

from quantum.optimizer import optimize_sensors
from quantum.classical_baseline import classical_sensor_fusion


st.set_page_config(
    page_title="Quantum Sensor Fusion",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Quantum-Enhanced Multi-Sensor Fusion")


if st.button("Generate New Scenario"):

    # --------------------------------------------------
    # Generate Environment
    # --------------------------------------------------

    environment = generate_environment()

    # --------------------------------------------------
    # Calculate Sensor Scores
    # --------------------------------------------------

    scores = calculate_sensor_scores(environment)

    # --------------------------------------------------
    # Merge data for AI model
    # --------------------------------------------------

    sensor_data = {
        **environment,
        **scores
    }

    # --------------------------------------------------
    # AI Prediction
    # --------------------------------------------------

    prediction, confidence = predict(sensor_data)

    # --------------------------------------------------
    # Quantum Optimization
    # --------------------------------------------------

    quantum = optimize_sensors(scores)

    # --------------------------------------------------
    # Classical Baseline
    # --------------------------------------------------

    classical = classical_sensor_fusion(scores)

    # --------------------------------------------------
    # Environment + Sensor Scores
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🌍 Environment")

        st.json(environment)

    with col2:

        st.subheader("📡 Sensor Scores")

        for sensor, score in scores.items():

            st.write(f"### {sensor}")

            st.progress(float(score))

            st.caption(f"{score:.2f}")

    st.divider()

    # --------------------------------------------------
    # AI Result
    # --------------------------------------------------

    st.subheader("🤖 AI Prediction")

    if prediction == 1:

        st.success(
            f"🎯 Target Detected ({confidence * 100:.2f}%)"
        )

    else:

        st.error(
            f"❌ No Target ({confidence * 100:.2f}%)"
        )

    st.divider()

    # --------------------------------------------------
    # Classical vs Quantum
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Classical Fusion")

        st.metric(
            "Fusion Score",
            classical["fusion_score"]
        )

        st.metric(
            "Detection",
            "Target" if classical["detected"] else "No Target"
        )

        st.write("Method:", classical["method"])

    with col2:

        st.subheader("⚛️ Quantum Fusion")

        st.metric(
            "Fusion Score",
            quantum["fusion_score"]
        )

        st.metric(
            "Objective",
            quantum["objective_value"]
        )

        st.metric(
            "Sensors Selected",
            quantum["selected_count"]
        )

        st.write("### Selected Sensors")

        if quantum["selected_sensors"]:

            for sensor in quantum["selected_sensors"]:
                st.success(sensor)

        else:

            st.warning("No sensors selected")

    st.divider()

    # --------------------------------------------------
    # Quantum Sensor Selection
    # --------------------------------------------------

    st.subheader("🛰️ Quantum Sensor Selection")

    for sensor, enabled in quantum["selection"].items():

        if enabled:
            st.success(f"✅ {sensor}")
        else:
            st.error(f"❌ {sensor}")