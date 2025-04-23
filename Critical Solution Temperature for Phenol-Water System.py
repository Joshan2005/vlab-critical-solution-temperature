import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Critical Solution Temperature Simulator", layout="centered")
st.title("🌡️ Critical Solution Temperature Simulator - Phenol-Water System")

# Theory Section
with st.expander("📘 AIM, PRINCIPLE & PROCEDURE"):
    st.markdown("""
    **AIM**  
    To determine the critical solution temperature (CST) for phenol-water system and the percentage of phenol in a given sample.

    **PRINCIPLE**  
    Phenol and water are partially miscible at ordinary temperatures. Their miscibility increases with temperature.  
    At a certain temperature, both phases become one homogeneous solution — this is called the **critical solution temperature**.

    **PROCEDURE**  
    1. Mix 5 ml of phenol with increasing volumes of distilled water (3 to 31 ml).  
    2. Heat the mixture in a water bath and note the temperature at which turbidity disappears.  
    3. Cool and record the temperature when turbidity reappears.  
    4. Repeat for all samples and plot Mean Temp vs % Phenol.
    """)

# Input Section
st.subheader("🔢 Enter Observations")

data = []
for i in range(1, 16):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        vol_water = st.number_input(f"#{i} - Volume of Water (ml)", value=3 + 2 * (i - 1), key=f"water_{i}")
    with col2:
        temp_dis = st.number_input(f"T_disappear (°C)", key=f"tdis_{i}")
    with col3:
        temp_app = st.number_input(f"T_appear (°C)", key=f"tapp_{i}")
    with col4:
        st.markdown("Mean Temp (°C):")
        mean_temp = (temp_dis + temp_app) / 2 if temp_dis and temp_app else 0
        st.write(f"**{mean_temp:.2f}**")
    if temp_dis and temp_app:
        vol_percent_phenol = (5 / (5 + vol_water)) * 100
        data.append((vol_percent_phenol, mean_temp))

# Unknown Sample
st.subheader("🧪 Unknown Sample")
unknown_temp_dis = st.number_input("Disappearance Temperature (°C)", key="unk_dis")
unknown_temp_app = st.number_input("Appearance Temperature (°C)", key="unk_app")
if unknown_temp_dis and unknown_temp_app:
    unknown_mean_temp = (unknown_temp_dis + unknown_temp_app) / 2
    st.write(f"**Mean Temp for Unknown Sample:** {unknown_mean_temp:.2f} °C")

# DataFrame and Plot
if data:
    df = pd.DataFrame(data, columns=["Volume % of Phenol", "Mean Temp (°C)"])
    st.subheader("📈 Mean Temperature vs Volume % Phenol")

    fig, ax = plt.subplots()
    ax.plot(df["Volume % of Phenol"], df["Mean Temp (°C)"], marker='o', color='green')
    ax.set_xlabel("Volume % of Phenol")
    ax.set_ylabel("Mean Temperature (°C)")
    ax.set_title("Critical Solution Temperature Curve")
    ax.grid(True)

    # Mark CST (maximum point)
    max_idx = df["Mean Temp (°C)"].idxmax()
    cst = df.iloc[max_idx]["Mean Temp (°C)"]
    critical_comp = df.iloc[max_idx]["Volume % of Phenol"]
    ax.axvline(critical_comp, color='red', linestyle='--')
    ax.annotate(f'CST = {cst:.2f}°C\n@ {critical_comp:.1f}%', 
                xy=(critical_comp, cst), xytext=(critical_comp+1, cst+1),
                arrowprops=dict(facecolor='red', shrink=0.05))
    st.pyplot(fig)

    # Result Section
    st.subheader("✅ Results")
    st.success(f"Critical Solution Temperature = **{cst:.2f} °C**")
    st.success(f"Critical Solution Composition = **{critical_comp:.1f} % Phenol**")

    # Estimating Phenol % in unknown sample
    if unknown_temp_dis and unknown_temp_app:
        closest_idx = (df["Mean Temp (°C)"] - unknown_mean_temp).abs().idxmin()
        est_phenol = df.iloc[closest_idx]["Volume % of Phenol"]
        st.success(f"Estimated % of Phenol in Unknown Sample = **{est_phenol:.1f} %**")

# Footer
st.info("Adjust input temperatures above to simulate different CST observations and see how the composition affects miscibility.")
