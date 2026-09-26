"""Sobel edge detection using NumPy """

from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from PIL import Image

SOBEL_GX = np.array(
    [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
    dtype=np.float32,
)
SOBEL_GY = np.array(
    [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
    dtype=np.float32,
)


def pil_to_rgb_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("RGB"), dtype=np.float32)


def to_grayscale(rgb: np.ndarray) -> np.ndarray:
    """Rec. 601 luminance; rgb is (H, W, 3)."""
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Same-size 2D convolution with edge padding."""
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
    windows = sliding_window_view(padded, (kh, kw))
    return np.einsum("ijkl,kl->ij", windows, kernel)


def sobel_magnitude(gray: np.ndarray) -> np.ndarray:
    """Gradient magnitude scaled to 0..255."""
    gx = convolve2d(gray, SOBEL_GX)
    gy = convolve2d(gray, SOBEL_GY)
    magnitude = np.hypot(gx, gy)
    peak = float(magnitude.max())
    if peak <= 0:
        return np.zeros_like(magnitude, dtype=np.float32)
    return (magnitude * (255.0 / peak)).astype(np.float32)


def apply_threshold(
    magnitude: np.ndarray,
    threshold: float,
    invert: bool = False,
) -> np.ndarray:
    """Binary edges: values >= threshold become 255 (or 0 if invert)."""
    edges = np.where(magnitude >= threshold, 255.0, 0.0).astype(np.uint8)
    if invert:
        return 255 - edges
    return edges


def detect_edges(image: Image.Image) -> np.ndarray:
    rgb = pil_to_rgb_array(image)
    gray = to_grayscale(rgb)
    return sobel_magnitude(gray)


def magnitude_to_pil(magnitude: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(magnitude, 0, 255).astype(np.uint8), mode="L")


def edges_to_pil(edges: np.ndarray) -> Image.Image:
    return Image.fromarray(edges, mode="L")
