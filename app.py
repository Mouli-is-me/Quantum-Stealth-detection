import streamlit as st

from simulator.sensor_simulator import (
    generate_environment,
    calculate_sensor_scores
)

from ai.predict import predict
from quantum.optimizer import optimize_sensors

st.set_page_config(
    page_title="Quantum Sensor Fusion",
    layout="wide"
)

st.title("🚀 Quantum-Enhanced Multi-Sensor Fusion")

if st.button("Generate New Scenario"):

    env = generate_environment()

    scores = calculate_sensor_scores(env)

    data = {
        **env,
        **scores
    }

    prediction, confidence = predict(data)

    selection = optimize_sensors(scores)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Environment")

        st.write(env)

    with col2:

        st.subheader("Sensor Scores")

        st.progress(scores["Radar"])

        st.write("Radar", scores["Radar"])

        st.progress(scores["Infrared"])

        st.write("Infrared", scores["Infrared"])

        st.progress(scores["Acoustic"])

        st.write("Acoustic", scores["Acoustic"])

    st.divider()

    st.subheader("AI Result")

    if prediction:

        st.success(
            f"Target Detected ({confidence*100:.2f}%)"
        )

    else:

        st.error(
            f"No Target ({confidence*100:.2f}%)"
        )

    st.divider()

    st.subheader("Quantum Decision")

    st.write(selection)