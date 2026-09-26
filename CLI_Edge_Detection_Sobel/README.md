# Image Edge Detector

Mini project: find edges in a photo with **NumPy** convolution and **Pillow**. The window is **Tkinter** (Python’s standard library).

## Layout

```text
Image_edge_detector/
  app.py                      # entry point
  requirements.txt
  README.md
  src/
    edge_detector/
      __init__.py             # public processing API
      processing.py           # grayscale, Sobel, threshold
      gui.py                  # Tkinter window
```

## How it works

1. Convert the image to grayscale (Rec. 601 luminance).
2. Convolve with Sobel kernels `Gx` and `Gy`.
3. Combine into a gradient magnitude and scale it to 0–255.
4. A threshold slider turns that map into a binary edge image.

Sobel already includes a little smoothing, so there is no extra blur step.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Use **Open image…** to pick a PNG, JPEG, BMP, or WebP file. Original and edges appear side by side. Move **Threshold** to keep only stronger edges. **Invert** switches white-on-black vs black-on-white. **Save edges…** writes a PNG of the current thresholded result.

Very large photos are resized (max side 1600 px) before Sobel so the app stays interactive; the on-screen preview is capped at 900 px.
