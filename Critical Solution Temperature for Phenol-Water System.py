import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Virtual Lab - Critical Solution Temperature", layout="centered")

st.title("🧪 Virtual Lab: Critical Solution Temperature of Phenol-Water System")

# -------------------------
# Aim, Apparatus, Principle
# -------------------------
with st.expander("📘 AIM, APPARATUS, PRINCIPLE & PROCEDURE"):
    st.markdown("""
    ### 🎯 AIM
    To determine the critical solution temperature for phenol-water system and to find out the percentage of phenol in the given sample.

    ### 🧪 APPARATUS
    Burette, boiling tube, thermometer, water bath, etc.

    ### 🧬 PRINCIPLE
    Phenol and water are partially miscible at ordinary temperatures. On shaking, two saturated solutions form (called conjugate solutions).  
    As temperature rises, mutual solubility increases until a homogeneous mixture forms — this temperature is called the **Critical Solution Temperature (CST)**.

    ### 🧂 PROCEDURE (Summary)
    1. Add 5 ml phenol + varying volumes of water (3–31 ml).
    2. Heat and stir in a water bath until turbidity disappears.
    3. Cool until turbidity reappears.
    4. Note both temperatures and compute mean.
    5. Repeat for all mixtures.
    """)

# -------------------------
# Observation Table
# -------------------------
st.subheader("📊 Observation Table Entry")

data = []
st.markdown("Enter disappearance and reappearance temperatures for each water volume:")

for i in range(15):
    water_vol = 3 + i * 2
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        t_dis = st.number_input(f"#{i+1} - T_disappear (°C)", key=f"dis_{i}")
    with col2:
        t_app = st.number_input(f"T_appear (°C)", key=f"app_{i}")
    with col3:
        if t_dis > 0 and t_app > 0:
            mean_temp = (t_dis + t_app) / 2
            vol_percent = (5 / (5 + water_vol)) * 100
            data.append((5, water_vol, vol_percent, t_dis, t_app, mean_temp))
            st.success(f"Mean Temp: {mean_temp:.2f} °C | Phenol %: {vol_percent:.2f}")
        else:
            st.warning("Enter both temperatures.")

# -------------------------
# Unknown Sample
# -------------------------
st.subheader("🧪 Unknown Sample")
unk_dis = st.number_input("T_disappear (°C) for Unknown", key="unk_dis")
unk_app = st.number_input("T_appear (°C) for Unknown", key="unk_app")
unk_mean = None
if unk_dis and unk_app:
    unk_mean = (unk_dis + unk_app) / 2
    st.success(f"Mean Temperature for Unknown Sample: **{unk_mean:.2f} °C**")

# -------------------------
# DataFrame and Graph
# -------------------------
if data:
    df = pd.DataFrame(data, columns=[
        "Vol. of Phenol (ml)", "Vol. of Water (ml)", "Vol. % Phenol",
        "T_disappear (°C)", "T_appear (°C)", "Mean Temp (°C)"
    ])

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Volume % of Phenol vs Mean Temperature")
    fig, ax = plt.subplots()
    ax.plot(df["Vol. % Phenol"], df["Mean Temp (°C)"], marker='o', linestyle='-', color='blue')
    ax.set_xlabel("Volume % of Phenol")
    ax.set_ylabel("Mean Temperature (°C)")
    ax.set_title("Critical Solution Temperature Curve")
    ax.grid(True)

    max_idx = df["Mean Temp (°C)"].idxmax()
    cst = df.loc[max_idx, "Mean Temp (°C)"]
    critical_comp = df.loc[max_idx, "Vol. % Phenol"]

    ax.axvline(x=critical_comp, color='red', linestyle='--', label="CST Point")
    ax.annotate(f"CST: {cst:.2f}°C\n@ {critical_comp:.1f}%", 
                xy=(critical_comp, cst), xytext=(critical_comp+1, cst+1),
                arrowprops=dict(facecolor='red', shrink=0.05), fontsize=9)
    st.pyplot(fig)

    # -------------------------
    # Result Section
    # -------------------------
    st.subheader("✅ Final Results")
    st.success(f"🧊 Critical Solution Temperature = **{cst:.2f} °C**")
    st.success(f"🧪 Critical Solution Composition = **{critical_comp:.1f} % Phenol**")

    if unk_mean:
        idx_closest = (df["Mean Temp (°C)"] - unk_mean).abs().idxmin()
        est_phenol = df.loc[idx_closest, "Vol. % Phenol"]
        st.success(f"🧬 Estimated % Phenol in Unknown Sample = **{est_phenol:.1f} %**")

# -------------------------
# Pre & Post Lab Qs
# -------------------------
with st.expander("🧠 Pre-Lab & Post-Lab Questions"):
    st.markdown("""
    **Pre-Lab Questions**
    1. Define partially miscible systems.  
    2. Define critical solution temperature.  
    3. How does temperature affect solubility of binary liquids?

    **Post-Lab Questions**
    1. List types of partially miscible systems.  
    2. Significance of critical solution temperature.  
    3. How does temperature affect phenol-water solubility?
    """)

# Footer
st.info("You can use this simulator to understand CST behavior by inputting various experimental values.")
