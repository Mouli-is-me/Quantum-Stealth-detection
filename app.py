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

    import time
    with st.status("Analyzing Battlefield Scenario...", expanded=True) as status:
        st.write("🌍 Generating environment factors...")
        time.sleep(0.5)
        environment = generate_environment()

        st.write("📡 Calculating multi-sensor confidence scores...")
        time.sleep(0.5)
        raw_scores = calculate_sensor_scores(environment)
        
        # Extract only the numeric sensor scores to prevent downstream crashes
        sensor_keys = ["Radar", "Infrared", "Acoustic", "Thermal", "EO_Camera"]
        scores = {k: float(v) for k, v in raw_scores.items() if k in sensor_keys}
        metadata = {k: v for k, v in raw_scores.items() if k not in sensor_keys}

        sensor_data = {
            **environment,
            **scores,
            **metadata
        }

        st.write("🤖 Running classical AI prediction model...")
        time.sleep(0.5)
        prediction, confidence = predict(sensor_data)

        st.write("⚡ Running Quantum Optimization & Classical Baseline in parallel...")
        time.sleep(0.5)
        
        import concurrent.futures
        import time
        
        start_parallel = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks to run concurrently
            future_quantum = executor.submit(optimize_sensors, scores)
            future_classical = executor.submit(classical_sensor_fusion, scores)
            
            # Wait for both to finish and retrieve results
            quantum = future_quantum.result()
            classical = future_classical.result()
            
        parallel_duration = time.time() - start_parallel

        status.update(label=f"Analysis Complete! (Parallel execution took {parallel_duration:.3f}s)", state="complete", expanded=False)

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
    # Parallel Execution Performance
    # --------------------------------------------------

    st.subheader("⚡ Parallel Execution Performance")
    
    st.info(
        f"**Concurrency achieved:** The Quantum Optimization Engine and Classical Baseline Fusion model were executed concurrently in separate threads. "
        f"Total parallel execution time: **{parallel_duration:.3f} seconds**."
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

    st.info(quantum["reason"])

    for sensor, enabled in quantum["selection"].items():

        if enabled:
            st.success(f"✅ {sensor}")
        else:
            st.error(f"❌ {sensor}")