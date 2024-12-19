def INB(p, lam, q_g, c_Rx, c_Dx, h_Dx, Se, Sp, p_Rx):
    """
    Calculate the incremental net benefit for a single diagnostic test.

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx (float): Cost of test.
        h_Dx (float): Harm of test.
        Se (float): Sensitivity of the test.
        Sp (float): Specificity of the test.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    
    kappa = c_Dx + lam * h_Dx
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return b * (p * Se - (1 - p) * (1 - Sp) * p_Rx / (1 - p_Rx)) - kappa
    elif p_Rx <= p <= 1:
        return b * (-p * (1 - Se) + (1 - p) * Sp * p_Rx / (1 - p_Rx)) - kappa

def INB_i_j_c(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, h_Dx_i, h_Dx_j, Se_i, Se_j, Sp_i, Sp_j, p_Rx):
    """
    Calculate the INB for two combined tests (conjunctive).

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx_i, c_Dx_j (float): Cost of test i and test j.
        h_Dx_i, h_Dx_j (float): Harm of test i and test j
        Se_i, Se_j (float): Sensitivity of test i and test j.
        Sp_i, Sp_j (float): Specificity of test i and test j.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i + lam * h_Dx_i + (p * Se_i + (1 - p) * (1 - Sp_i)) * (c_Dx_j + lam * h_Dx_j)
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return -kappa + b * (p * Se_i * Se_j - (1 - p) * (1 - Sp_i) * (1 - Sp_j) * p_Rx / (1 - p_Rx))
    elif p_Rx <= p <= 1:
        return -kappa + b * (-p * (1 - Se_i * Se_j) + (1 - p) * (1 - (1 - Sp_i) * (1 - Sp_j)) * p_Rx / (1 - p_Rx))
        
def INB_i_j_k_c(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (conjunctive).

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx_i, c_Dx_j, c_Dx_k (float): Cost of test i, j, and k.
        h_Dx_i, h_Dx_j, h_Dx_k (float): Harm of test i, j, and k.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i + lam * h_Dx_i + (p * Se_i + (1 - p) * (1 - Sp_i)) * (c_Dx_j + lam * h_Dx_j) + \
            (p * Se_i * Se_j + (1 - p) * (1 - Sp_i) * (1 - Sp_j)) * (c_Dx_k + lam * h_Dx_k)
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return (
            -kappa + b * (p * Se_i * Se_j * Se_k
            - (1 - p) * (1 - Sp_i) * (1 - Sp_j) * (1 - Sp_k) * p_Rx / (1 - p_Rx))
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            + b * (-p * (1 - Se_i * Se_j * Se_k)
            + (1 - p) * (1 - (1 - Sp_i) * (1 - Sp_j) * (1 - Sp_k)) * p_Rx / (1 - p_Rx))
        )


def INB_i_j_d(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, h_Dx_i, h_Dx_j, Se_i, Se_j, Sp_i, Sp_j, p_Rx):
    """
    Calculate the INB for two combined tests (disjunctive).

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx_i, c_Dx_j (float): Cost of test i.
        h_Dx_i, h_Dx_j (float): Harm of test i.
        Se_i, Se_j (float): Sensitivity of test i and test j.
        Sp_i, Sp_j (float): Specificity of test i and test j.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i + lam * h_Dx_i + (p * (1 - Se_i) + (1 - p) * Sp_i) * (c_Dx_j + lam * h_Dx_j)
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return (
            -kappa + b * (p * (1 - (1 - Se_i) * (1 - Se_j))
            - (1 - p) * (1 - Sp_i * Sp_j) * p_Rx / (1 - p_Rx))
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            + b * (-p * (1 - Se_i) * (1 - Se_j)
            + (1 - p) * Sp_i * Sp_j * p_Rx / (1 - p_Rx))
        )


def INB_i_j_k_d(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (disjunctive).

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx_i, c_Dx_j, c_Dx_k (float): Cost of test i, j, and k.
        h_Dx_i, h_Dx_j, h_Dx_k (float): Harm of test i, j, and k.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i + lam * h_Dx_i + (p * (1 - Se_i) + (1 - p) * Sp_i) * (c_Dx_j + lam * h_Dx_j) + \
            (p * (1 - Se_i) * (1 - Se_j) + (1 - p) * Sp_i * Sp_j) * (c_Dx_k + lam * h_Dx_k)
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return (
            -kappa + b * (p * (1 - (1 - Se_i) * (1 - Se_j) * (1 - Se_k))
            - (1 - p) * (1 - Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx))
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            + b * (-p * (1 - Se_i) * (1 - Se_j) * (1 - Se_k)
            + (1 - p) * Sp_i * Sp_j * Sp_k * p_Rx / (1 - p_Rx))
        )


def INB_i_j_k_M(p, lam, q_g, c_Rx, c_Dx_i, c_Dx_j, c_Dx_k, h_Dx_i, h_Dx_j, h_Dx_k, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (disjunctive).

    Parameters:
        p (float): Probability of illness.
        lam (float): Willingness to pay for a QALY.
        q_g (float): QALY gain.
        c_Rx (float): Treament cost.
        c_Dx_i, c_Dx_j, c_Dx_k (float): Cost of test i, j, and k.
        h_Dx_i, h_Dx_j, h_Dx_k (float): Harm of test i, j, and k.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i + lam * h_Dx_i + c_Dx_j + lam * h_Dx_j + \
            (p * Se_i * (1 - Se_j) + p * (1 - Se_i) * Se_j + \
            (1 - p) * Sp_i * (1 - Sp_j) + (1 - p) * (1 - Sp_i) * Sp_j) * (c_Dx_k + lam * h_Dx_k)
    b = lam * q_g - c_Rx
    
    if 0 <= p < p_Rx:
        return (
            -kappa + b * (p * (Se_i * Se_j + Se_i * Se_k + Se_j * Se_k - 2 * Se_i * Se_j * Se_k)
            - (1 - p) * (1 - Sp_i * Sp_j - Sp_i * Sp_k - Sp_j * Sp_k + 2 * Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx))
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            + b * (-p * (1 - Se_i * Se_j - Se_i * Se_k - Se_j * Se_k + 2 * Se_i * Se_j * Se_k)
            + (1 - p) * (Sp_i * Sp_j + Sp_i * Sp_k + Sp_j * Sp_k - 2 * Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx))
        )

