import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utilities.inb_utils import *

def main():
    st.title("Visualizing the incremental net benefit (INB) of combined tests")
    st.markdown("""
    This app plots the incremental net benefit (INB) for different types of diagnostic tests.
    Users can customize test parameters and probabilities of illness to visualize their INBs.
    """)

    st.sidebar.header("Parameters")

    # probability of illness
    p_min = st.sidebar.slider(r"Minimum probability of illness ($p$)", 0.0, 1.0, 0.0, 0.01)
    p_max = st.sidebar.slider(r"Maximum probability of illness ($p$)", 0.0, 1.0, 1.0, 0.01)
    p_values = np.linspace(p_min, p_max, 100)

    # treatment threshold
    p_Rx = st.sidebar.slider(r"Treatment threshold ($p^{\rm Rx}$)", 0.0, 1.0, 0.5, 0.01)

    # test parameters 1
    st.sidebar.subheader("Parameters of test 1")
    Se = st.sidebar.slider(r"Sensitivity (${\rm Se}_1$)", 0.0, 1.0, 0.8, 0.01)
    Sp = st.sidebar.slider(r"Specificity (${\rm Sp}_1$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_d_b = st.sidebar.number_input(r"Cost-benefit ratio of test 1 ($c_1^\mathrm{Dx}/b$)", 0.0, 1.0, 0.1, 0.01)

    # tests parameters 2
    st.sidebar.subheader("Parameters of test 2")
    Se_j = st.sidebar.slider(r"Sensitivity (${\rm Se}_2$)", 0.0, 1.0, 0.8, 0.01)
    Sp_j = st.sidebar.slider(r"Specificity (${\rm Sp}_2$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_j_d_b = st.sidebar.number_input(r"Cost-benefit ratio of test 2 ($c_2^\mathrm{Dx}/b$)", 0.0, 1.0, 0.1, 0.01)

    # tests parameters 3
    st.sidebar.subheader("Parameters of test 3")
    Se_k = st.sidebar.slider(r"Sensitivity (${\rm Se}_3$)", 0.0, 1.0, 0.8, 0.01)
    Sp_k = st.sidebar.slider(r"Specificity (${\rm Sp}_3$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_k_d_b = st.sidebar.number_input(r"Cost-benefit ratio of test 3 ($c_3^\mathrm{Dx}/b$)", 0.0, 1.0, 0.1, 0.01)
    
    # user selects the INB type
    st.sidebar.subheader("Select INB type")
    selected_INBs = st.sidebar.multiselect(
        "Choose INBs to plot",
        ["INB (single)", "INB (dual, conjunctive)", "INB (dual, disjunctive)",\
        "INB (triple, conjunctive)", "INB (triple, disjunctive)", "INB (triple, majority)"],
        default=["INB (single)"]
    )

    # ======================= PLOTTING RESULTS =======================
    fig, ax = plt.subplots()
    ax.axvline(p_Rx, color="Grey", linestyle="--", label=r"treatment threshold ($p^{\rm Rx} = %1.2f$)"%p_Rx)

    INB_functions = {
    "INB (single)": lambda p: INB_d_b(p, c_Dx_d_b, Se, Sp, p_Rx),
    "INB (dual, conjunctive)": lambda p: INB_d_b_i_j_c(p, c_Dx_d_b, c_Dx_j_d_b, Se, Se_j, Sp, Sp_j, p_Rx),
    "INB (dual, disjunctive)": lambda p: INB_d_b_i_j_d(p, c_Dx_d_b, c_Dx_j_d_b, Se, Se_j, Sp, Sp_j, p_Rx),
    "INB (triple, conjunctive)": lambda p: INB_d_b_i_j_k_c(p, c_Dx_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se, Se_j, Se_k, Sp, Sp_j, Sp_k, p_Rx),
    "INB (triple, disjunctive)": lambda p: INB_d_b_i_j_k_d(p, c_Dx_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se, Se_j, Se_k, Sp, Sp_j, Sp_k, p_Rx),
    "INB (triple, majority)": lambda p: INB_d_b_i_j_k_M(p, c_Dx_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se, Se_j, Se_k, Sp, Sp_j, Sp_k, p_Rx)
    }

    for INB_type in selected_INBs:
        if INB_type in INB_functions:
            y_values = [INB_functions[INB_type](p) for p in p_values]
            ax.plot(p_values, y_values, label=f"{INB_type}")

    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)

    ax.set_xlabel("probability of illness (p)")
    ax.set_ylabel("incremental net benefit (INB)")
    ax.legend(loc="best", fontsize=10)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
