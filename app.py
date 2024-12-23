import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utilities.inb_utils import *
from utilities.inb_d_b_utils import *

def page1():
    st.title("Visualizing the incremental net benefit (INB) of combined tests")
    st.markdown("""
    This app plots the incremental net benefit (INB) for different types of diagnostic tests.
    Users can customize test parameters and probabilities of illness to visualize their INBs.
    
    In this parameterization, we exclude parameters that represent the harm caused by a test
    and a patient's willingness to pay for a quality-adjusted life year, and we normalize all 
    quantities based on the treatment's net benefit.
    """)

    st.sidebar.header("Parameters")

    # probability of illness
    p_min = st.sidebar.slider(r"Minimum probability of illness ($p$)", 0.0, 1.0, 0.0, 0.01)
    p_max = st.sidebar.slider(r"Maximum probability of illness ($p$)", 0.0, 1.0, 1.0, 0.01)
    p_values = np.linspace(p_min, p_max, 1000)

    # treatment threshold
    p_Rx = st.sidebar.slider(r"Treatment threshold ($\tilde{p}^{\rm Rx}$)", 0.0, 1.0, 0.5, 0.01)

    # test parameters 1
    st.sidebar.subheader("Parameters of test 1")
    Se_i = st.sidebar.slider(r"Sensitivity (${\rm Se}_1$)", 0.0, 1.0, 0.8, 0.01)
    Sp_i = st.sidebar.slider(r"Specificity (${\rm Sp}_1$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_i_d_b = st.sidebar.number_input(r"Cost-benefit ratio of test 1 ($c_1^\mathrm{Dx}/b$)", 0.0, 1.0, 0.1, 0.01)

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
    ax.axvline(p_Rx, color="Grey", linestyle="--", label=r"$\tilde{p}^{\rm Rx} = %1.2f$"%p_Rx)

    INB_functions = {
    "INB (single)": lambda p: INB_d_b(p, c_Dx_i_d_b, Se_i, Sp_i, p_Rx),
    "INB (dual, conjunctive)": lambda p: INB_d_b_i_j_c(p, c_Dx_i_d_b, c_Dx_j_d_b, Se_i, Se_j, Sp_i, Sp_j, p_Rx),
    "INB (dual, disjunctive)": lambda p: INB_d_b_i_j_d(p, c_Dx_i_d_b, c_Dx_j_d_b, Se_i, Se_j, Sp_i, Sp_j, p_Rx),
    "INB (triple, conjunctive)": lambda p: INB_d_b_i_j_k_c(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx),
    "INB (triple, disjunctive)": lambda p: INB_d_b_i_j_k_d(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx),
    "INB (triple, majority)": lambda p: INB_d_b_i_j_k_M(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx)
    }

    y_all_values = []
    for INB_type in selected_INBs:
        if INB_type in INB_functions:
            y_values = [INB_functions[INB_type](p) for p in p_values]
            y_all_values.append(y_values)
            y_values = np.asarray(y_values)
            ax.plot(p_values[y_values >= 0], y_values[y_values >= 0], label=f"{INB_type}", zorder=2)
    
    y_max_values = np.max(y_all_values, axis=0)
    ax.plot(p_values[y_max_values >= 0], y_max_values[y_max_values >= 0], \
            color="k", linewidth=5, label=f"INB hull", alpha=0.4, zorder=1)    
    
    ax.set_xlim(0,1)
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)

    ax.set_xlabel("probability of illness (p)")
    ax.set_ylabel("incremental net benefit (INB)")
    ax.legend(loc="best", fontsize=10)
    st.pyplot(fig)
    
def page2():
    st.title("Visualizing the incremental net benefit (INB) of combined tests")
    st.markdown("""
    This app plots the incremental net benefit (INB) for different types of diagnostic tests.
    Users can customize test parameters and probabilities of illness to visualize their INBs.
    
    In this parameterization, we include parameters that represent the harm caused by a test
    and a patient's willingness to pay for a quality-adjusted life year.
    """)

    st.sidebar.header("Parameters")

    # probability of illness
    p_min = st.sidebar.slider(r"Minimum probability of illness ($p$)", 0.0, 1.0, 0.0, 0.01)
    p_max = st.sidebar.slider(r"Maximum probability of illness ($p$)", 0.0, 1.0, 1.0, 0.01)
    p_values = np.linspace(p_min, p_max, 1000)

    # willingness to pay for a QALY
    lam = st.sidebar.slider(r"Willingness to pay for a QALY ($\lambda$)", 0.0, 1.0, 0.9, 0.01)

    # QALY gain
    q_g = st.sidebar.slider(r"QALY gain ($q_{\rm g}$)", 0.0, 1.0, 0.9, 0.01)
    
    # treament cost
    c_Rx = st.sidebar.slider(r"Treatment cost ($c^{\rm Rx}$)", 0.0, 1.0, 0.05, 0.01)
        
    # treatment threshold
    p_Rx = st.sidebar.slider(r"Treatment threshold ($\tilde{p}^{\rm Rx}$)", 0.0, 1.0, 0.5, 0.01)

    # test parameters 1
    st.sidebar.subheader("Parameters of test 1")
    Se_i = st.sidebar.slider(r"Sensitivity (${\rm Se}_1$)", 0.0, 1.0, 0.8, 0.01)
    Sp_i = st.sidebar.slider(r"Specificity (${\rm Sp}_1$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_i = st.sidebar.number_input(r"Cost of test 1 ($c_1^\mathrm{Dx}$)", 0.0, 1.0, 0.1, 0.01)
    h_Dx_i = st.sidebar.number_input(r"Harm of test 1 ($h_1^\mathrm{Dx}$)", 0.0, 1.0, 0.01, 0.01)
    
    # tests parameters 2
    st.sidebar.subheader("Parameters of test 2")
    Se_j = st.sidebar.slider(r"Sensitivity (${\rm Se}_2$)", 0.0, 1.0, 0.8, 0.01)
    Sp_j = st.sidebar.slider(r"Specificity (${\rm Sp}_2$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_j = st.sidebar.number_input(r"Cost of test 2 ($c_2^\mathrm{Dx}$)", 0.0, 1.0, 0.1, 0.01)
    h_Dx_j = st.sidebar.number_input(r"Harm of test 2 ($h_1^\mathrm{Dx}$)", 0.0, 1.0, 0.01, 0.01)
    
    # tests parameters 3
    st.sidebar.subheader("Parameters of test 3")
    Se_k = st.sidebar.slider(r"Sensitivity (${\rm Se}_3$)", 0.0, 1.0, 0.8, 0.01)
    Sp_k = st.sidebar.slider(r"Specificity (${\rm Sp}_3$)", 0.0, 1.0, 0.8, 0.01)
    c_Dx_k = st.sidebar.number_input(r"Cost of test 3 ($c_3^\mathrm{Dx}$)", 0.0, 1.0, 0.1, 0.01)
    h_Dx_k = st.sidebar.number_input(r"Harm of test 3 ($h_3^\mathrm{Dx}$)", 0.0, 1.0, 0.01, 0.01)
        
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
    ax.axvline(p_Rx, color="Grey", linestyle="--", label=r"$\tilde{p}^{\rm Rx} = %1.2f$"%p_Rx)

    INB_functions = {
    "INB (single)": lambda p: INB(p, lam, q_g, c_Rx, c_Dx_i, h_Dx_i, Se_i, Sp_i, p_Rx),
    "INB (dual, conjunctive)": lambda p: INB_i_j_c(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, h_Dx_i, h_Dx_j, Se_i, Se_j, Sp_i, Sp_j, p_Rx),
    "INB (dual, disjunctive)": lambda p: INB_i_j_d(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, h_Dx_i, h_Dx_j, Se_i, Se_j, Sp_i, Sp_j, p_Rx),
    "INB (triple, conjunctive)": lambda p: INB_i_j_k_c(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx),
    "INB (triple, disjunctive)": lambda p: INB_i_j_k_d(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx),
    "INB (triple, majority)": lambda p: INB_i_j_k_M(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx)
    }

    y_all_values = []
    for INB_type in selected_INBs:
        if INB_type in INB_functions:
            y_values = [INB_functions[INB_type](p) for p in p_values]
            y_all_values.append(y_values)
            y_values = np.asarray(y_values)
            ax.plot(p_values[y_values >= 0], y_values[y_values >= 0], label=f"{INB_type}", zorder=2)
    
    y_max_values = np.max(y_all_values, axis=0)
    ax.plot(p_values[y_max_values >= 0], y_max_values[y_max_values >= 0], \
            color="k", linewidth=5, label=f"INB hull", alpha=0.4, zorder=1)    
    
    ax.set_xlim(0,1)
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)

    ax.set_xlabel("probability of illness (p)")
    ax.set_ylabel("incremental net benefit (INB)")
    ax.legend(loc="best", fontsize=10)
    st.pyplot(fig)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select between two parameterizations:", ["Parameterization 1", "Parameterization 2"])

    if page == "Parameterization 1":
        page1()
    elif page == "Parameterization 2":
        page2()

if __name__ == "__main__":
    main()

