"""Sobel edge detection (NumPy + Pillow) with an optional Tkinter viewer."""

from edge_detector.processing import (
    apply_threshold,
    convolve2d,
    detect_edges,
    edges_to_pil,
    magnitude_to_pil,
    pil_to_rgb_array,
    sobel_magnitude,
    to_grayscale,
)

__all__ = [
    "apply_threshold",
    "convolve2d",
    "detect_edges",
    "edges_to_pil",
    "magnitude_to_pil",
    "pil_to_rgb_array",
    "sobel_magnitude",
    "to_grayscale",
]
