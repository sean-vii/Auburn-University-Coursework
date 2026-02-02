import numpy as np

def _pair(x):
    if isinstance(x, (tuple, list)) and len(x) == 2:
        return int(x[0]), int(x[1])
    return int(x), int(x)

def im2col(x, kH, kW, stride=1, padding=0, dilation=1):
    """TODO: Convert 2D convolution into matrix multiplication via columnization.
    Args:
        x: (C, H, W) input
        kH, kW: kernel height/width
        stride: int or (sH, sW)
        padding: int or (pH, pW)
        dilation: int or (dH, dW)
    Returns:
        cols: (C*kH*kW, outH*outW)
    Steps to implement:
      1) Parse stride/padding/dilation with _pair (provided).
      2) Compute effective kernel size with dilation.
      3) Compute out spatial dims (H_out, W_out) and pad the input.
      4) Extract each sliding window into a column and stack.
    """
    x = np.asarray(x)
    if x.ndim != 3:
        raise ValueError("Input x must have shape (C, H, W)")

    sH, sW = _pair(stride)
    pH, pW = _pair(padding)
    dH, dW = _pair(dilation)

    C, H, W = x.shape

    kH_eff = (kH - 1) * dH + 1
    kW_eff = (kW - 1) * dW + 1

    H_out = (H + 2 * pH - kH_eff) // sH + 1
    W_out = (W + 2 * pW - kW_eff) // sW + 1
    if H_out <= 0 or W_out <= 0:
        raise ValueError("Invalid configuration leading to non-positive output size")

    x_padded = np.pad(x, ((0, 0), (pH, pH), (pW, pW)), mode='constant')

    cols = np.empty((C * kH * kW, H_out * W_out), dtype=x_padded.dtype)

    col_idx = 0
    for oh in range(H_out):
        h_start = oh * sH
        h_end = h_start + kH_eff
        for ow in range(W_out):
            w_start = ow * sW
            w_end = w_start + kW_eff
            window = x_padded[:, h_start:h_end:dH, w_start:w_end:dW]
            cols[:, col_idx] = window.reshape(-1)
            col_idx += 1

    return cols
