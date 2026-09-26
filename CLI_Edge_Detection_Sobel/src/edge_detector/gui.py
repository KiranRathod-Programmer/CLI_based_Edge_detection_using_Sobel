"""Tkinter viewer for Sobel edge detection."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from PIL import Image, ImageTk

from edge_detector.processing import apply_threshold, detect_edges, edges_to_pil

DISPLAY_MAX_SIDE = 900
PROCESS_MAX_SIDE = 1600
IMAGE_TYPES = [
    ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
    ("All files", "*.*"),
]


def fit_image(image: Image.Image, max_side: int) -> Image.Image:
    w, h = image.size
    longest = max(w, h)
    if longest <= max_side:
        return image
    scale = max_side / longest
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    return image.resize(new_size, Image.Resampling.LANCZOS)


class EdgeDetectorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Image Edge Detector")
        self.root.minsize(720, 480)

        self.source_path: Optional[str] = None
        self.display_original: Optional[Image.Image] = None
        self.working_original: Optional[Image.Image] = None
        self.magnitude = None
        self.edges_image: Optional[Image.Image] = None
        self._photo_original: Optional[ImageTk.PhotoImage] = None
        self._photo_edges: Optional[ImageTk.PhotoImage] = None

        self.threshold = tk.IntVar(value=40)
        self.invert = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(fill=tk.X)

        ttk.Button(toolbar, text="Open image…", command=self.open_image).pack(
            side=tk.LEFT
        )
        ttk.Button(toolbar, text="Save edges…", command=self.save_edges).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Checkbutton(
            toolbar,
            text="Invert (black on white)",
            variable=self.invert,
            command=self.refresh_edges,
        ).pack(side=tk.LEFT, padx=(16, 0))

        slider_row = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        slider_row.pack(fill=tk.X)
        ttk.Label(slider_row, text="Threshold").pack(side=tk.LEFT)
        self.threshold_label = ttk.Label(slider_row, text="40", width=4)
        self.threshold_label.pack(side=tk.RIGHT)
        self.slider = ttk.Scale(
            slider_row,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.threshold,
            command=self._on_threshold,
        )
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)

        panels = ttk.Frame(self.root, padding=8)
        panels.pack(fill=tk.BOTH, expand=True)
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)
        panels.rowconfigure(1, weight=1)

        ttk.Label(panels, text="Original", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(panels, text="Edges (Sobel)", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=1, sticky="w"
        )

        self.original_label = ttk.Label(
            panels, text="Open an image to begin", anchor=tk.CENTER
        )
        self.original_label.grid(row=1, column=0, sticky="nsew", padx=(0, 4))
        self.edges_label = ttk.Label(panels, text="", anchor=tk.CENTER)
        self.edges_label.grid(row=1, column=1, sticky="nsew", padx=(4, 0))

        self.status = ttk.Label(
            self.root, text="Ready — Sobel edge detector", padding=8
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def _on_threshold(self, _value: str) -> None:
        value = int(float(self.threshold.get()))
        self.threshold_label.config(text=str(value))
        self.refresh_edges()

    def open_image(self) -> None:
        path = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
        if not path:
            return
        try:
            image = Image.open(path)
            image.load()
        except OSError as exc:
            messagebox.showerror("Could not open image", str(exc))
            return

        self.source_path = path
        rgb = image.convert("RGB")
        self.working_original = fit_image(rgb, PROCESS_MAX_SIDE)
        self.display_original = fit_image(self.working_original, DISPLAY_MAX_SIDE)
        self.magnitude = detect_edges(self.working_original)

        self._show_pil(self.original_label, self.display_original, original=True)
        self.refresh_edges()
        w, h = self.working_original.size
        self.status.config(
            text=f"Sobel  |  {w}×{h} px working size  |  {path}"
        )

    def refresh_edges(self) -> None:
        if self.magnitude is None:
            return
        threshold = int(float(self.threshold.get()))
        edges = apply_threshold(self.magnitude, threshold, invert=self.invert.get())
        self.edges_image = edges_to_pil(edges)
        display_edges = fit_image(self.edges_image, DISPLAY_MAX_SIDE)
        self._show_pil(self.edges_label, display_edges, original=False)

    def save_edges(self) -> None:
        if self.edges_image is None:
            messagebox.showinfo("Nothing to save", "Open an image first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.edges_image.save(path)
        except OSError as exc:
            messagebox.showerror("Could not save", str(exc))
            return
        self.status.config(text=f"Saved edges to {path}")

    def _show_pil(
        self, widget: ttk.Label, image: Image.Image, *, original: bool
    ) -> None:
        photo = ImageTk.PhotoImage(image)
        if original:
            self._photo_original = photo
        else:
            self._photo_edges = photo
        widget.config(image=photo, text="")


def main() -> None:
    root = tk.Tk()
    EdgeDetectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
