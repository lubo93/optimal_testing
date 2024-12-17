def INB_d_b(p, c_Dx_d_b, Se, Sp, p_Rx):
    """
    Calculate the incremental net benefit for a single diagnostic test.

    Parameters:
        p (float): Probability of illness.
        c_Dx_d_b (float): Cost of test divided by benefit.
        Se (float): Sensitivity of the test.
        Sp (float): Specificity of the test.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    if 0 <= p < p_Rx:
        return p * Se - (1 - p) * (1 - Sp) * p_Rx / (1 - p_Rx) - c_Dx_d_b
    elif p_Rx <= p <= 1:
        return -p * (1 - Se) + (1 - p) * Sp * p_Rx / (1 - p_Rx) - c_Dx_d_b

def INB_d_b_i_j_c(p, c_Dx_i_d_b, c_Dx_j_d_b, Se_i, Se_j, Sp_i, Sp_j, p_Rx):
    """
    Calculate the INB for two combined tests (complementary) considering costs.

    Parameters:
        p (float): Probability of illness.
        c_Dx_i_d_b (float): Cost of test i.
        c_Dx_j_d_b (float): Cost of test j.
        Se_i, Se_j (float): Sensitivity of test i and test j.
        Sp_i, Sp_j (float): Specificity of test i and test j.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i_d_b + (p * Se_i + (1 - p) * (1 - Sp_i)) * c_Dx_j_d_b
    if 0 <= p < p_Rx:
        return -kappa + p * Se_i * Se_j - (1 - p) * (1 - Sp_i) * (1 - Sp_j) * p_Rx / (1 - p_Rx)
    elif p_Rx <= p <= 1:
        return -kappa - p * (1 - Se_i * Se_j) + (1 - p) * (1 - (1 - Sp_i) * (1 - Sp_j)) * p_Rx / (1 - p_Rx)
        
def INB_d_b_i_j_k_c(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (complementary) considering costs.

    Parameters:
        p (float): Probability of illness.
        c_Dx_i_d_b (float): Cost of test i divided by benefit.
        c_Dx_j_d_b (float): Cost of test j divided by benefit.
        c_Dx_k_d_b (float): Cost of test k divided by benefit.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i_d_b + (p * Se_i + (1 - p) * (1 - Sp_i)) * c_Dx_j_d_b + \
            (p * Se_i * Se_j + (1 - p) * (1 - Sp_i) * (1 - Sp_j)) * c_Dx_k_d_b

    if 0 <= p < p_Rx:
        return (
            -kappa + p * Se_i * Se_j * Se_k
            - (1 - p) * (1 - Sp_i) * (1 - Sp_j) * (1 - Sp_k) * p_Rx / (1 - p_Rx)
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            - p * (1 - Se_i * Se_j * Se_k)
            + (1 - p) * (1 - (1 - Sp_i) * (1 - Sp_j) * (1 - Sp_k)) * p_Rx / (1 - p_Rx)
        )


def INB_d_b_i_j_d(p, c_Dx_i_d_b, c_Dx_j_d_b, Se_i, Se_j, Sp_i, Sp_j, p_Rx):
    """
    Calculate the INB for two combined tests (serial testing).

    Parameters:
        p (float): Probability of illness.
        c_Dx_i_d_b (float): Cost of test i divided by benefit.
        c_Dx_j_d_b (float): Cost of test j divided by benefit.
        Se_i, Se_j (float): Sensitivity of tests i and j.
        Sp_i, Sp_j (float): Specificity of tests i and j.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i_d_b + (p * (1 - Se_i) + (1 - p) * Sp_i) * c_Dx_j_d_b

    if 0 <= p < p_Rx:
        return (
            -kappa + p * (1 - (1 - Se_i) * (1 - Se_j))
            - (1 - p) * (1 - Sp_i * Sp_j) * p_Rx / (1 - p_Rx)
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            - p * (1 - Se_i) * (1 - Se_j)
            + (1 - p) * Sp_i * Sp_j * p_Rx / (1 - p_Rx)
        )


def INB_d_b_i_j_k_d(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (serial testing).

    Parameters:
        p (float): Probability of illness.
        c_Dx_i_d_b (float): Cost of test i divided by benefit.
        c_Dx_j_d_b (float): Cost of test j divided by benefit.
        c_Dx_k_d_b (float): Cost of test k divided by benefit.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i_d_b + (p * (1 - Se_i) + (1 - p) * Sp_i) * c_Dx_j_d_b + \
            (p * (1 - Se_i) * (1 - Se_j) + (1 - p) * Sp_i * Sp_j) * c_Dx_k_d_b

    if 0 <= p < p_Rx:
        return (
            -kappa + p * (1 - (1 - Se_i) * (1 - Se_j) * (1 - Se_k))
            - (1 - p) * (1 - Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx)
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            - p * (1 - Se_i) * (1 - Se_j) * (1 - Se_k)
            + (1 - p) * Sp_i * Sp_j * Sp_k * p_Rx / (1 - p_Rx)
        )


def INB_d_b_i_j_k_M(p, c_Dx_i_d_b, c_Dx_j_d_b, c_Dx_k_d_b, Se_i, Se_j, Se_k, Sp_i, Sp_j, Sp_k, p_Rx):
    """
    Calculate the INB for three combined tests (majority testing strategy).

    Parameters:
        p (float): Probability of illness.
        c_Dx_i_d_b (float): Cost of test i divided by benefit.
        c_Dx_j_d_b (float): Cost of test j divided by benefit.
        c_Dx_k_d_b (float): Cost of test k divided by benefit.
        Se_i, Se_j, Se_k (float): Sensitivity of tests i, j, and k.
        Sp_i, Sp_j, Sp_k (float): Specificity of tests i, j, and k.
        p_Rx (float): Treatment threshold.

    Returns:
        float: Incremental net benefit value.
    """
    kappa = c_Dx_i_d_b + c_Dx_j_d_b + (p * Se_i * (1 - Se_j) + p * (1 - Se_i) * Se_j +
                                      (1 - p) * Sp_i * (1 - Sp_j) + (1 - p) * (1 - Sp_i) * Sp_j) * c_Dx_k_d_b

    if 0 <= p < p_Rx:
        return (
            -kappa + p * (Se_i * Se_j + Se_i * Se_k + Se_j * Se_k - 2 * Se_i * Se_j * Se_k)
            - (1 - p) * (1 - Sp_i * Sp_j - Sp_i * Sp_k - Sp_j * Sp_k + 2 * Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx)
        )
    elif p_Rx <= p <= 1:
        return (
            -kappa
            - p * (1 - Se_i * Se_j - Se_i * Se_k - Se_j * Se_k + 2 * Se_i * Se_j * Se_k)
            + (1 - p) * (Sp_i * Sp_j + Sp_i * Sp_k + Sp_j * Sp_k - 2 * Sp_i * Sp_j * Sp_k) * p_Rx / (1 - p_Rx)
        )

