import numpy as np
from im2col import im2col, _pair

def conv2d_im2col(img, weight, bias=0.0, stride=1, padding=0, dilation=1):
    """TODO: Convolve a grayscale image with filters using im2col.
    Args:
        img: (H, W) in [0,1]
        weight: (C_out, 1, kH, kW)
        bias: float or (C_out,)
    Returns:
        out: (C_out, H_out, W_out)
    Steps to implement:
      1) Use im2col to get columns of shape (kH*kW, outHW).
      2) Reshape weight to (C_out, kH*kW) and matrix-multiply.
      3) Add bias and reshape back to (C_out, H_out, W_out).
    """
    # TODO: your code here
    if img.ndim != 2:
        raise ValueError("img must be 2D (grayscale)")

    C_out, C_in, kH, kW = weight.shape
    if C_in != 1:
        raise ValueError("Expected single-channel weights with shape (C_out, 1, kH, kW)")

    sH, sW = _pair(stride)
    pH, pW = _pair(padding)
    dH, dW = _pair(dilation)

    cols = im2col(img[np.newaxis, :, :], kH, kW, stride=stride, padding=padding, dilation=dilation)

    kH_eff = (kH - 1) * dH + 1
    kW_eff = (kW - 1) * dW + 1
    H, W = img.shape
    H_out = (H + 2 * pH - kH_eff) // sH + 1
    W_out = (W + 2 * pW - kW_eff) // sW + 1

    weight_mat = weight.reshape(C_out, -1)
    out = weight_mat @ cols

    if np.isscalar(bias):
        out += bias
    else:
        bias = np.asarray(bias).reshape(-1, 1)
        out += bias

    return out.reshape(C_out, H_out, W_out)

def kernels():
    gaussian_3x3 = (1/16.0) * np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32)
    sharpen_3x3  = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)
    sobel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)
    sobel_y = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)
    def pack(*mats):
        return np.stack([m[np.newaxis, :, :] for m in mats], axis=0)
    return {
        "gaussian_3x3": pack(gaussian_3x3),
        "sharpen_3x3":  pack(sharpen_3x3),
        "sobel_x":      pack(sobel_x),
        "sobel_y":      pack(sobel_y),
    }
