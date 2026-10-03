"""Score image-model redraws against a true silhouette mask (a screen, not a verdict).

    python silhouette_qa.py MASK.png CANDIDATE.png [CANDIDATE2.png ...] [--overlay-dir out/]

MASK: a white-on-black silhouette of the subject at the exact camera (for example an object-id render
from your previs). Each candidate is segmented as "craft" pixels (not near-black, not blue-dominant
space) and compared with the mask:

  raw_iou       IoU at the given framing
  aligned_iou   best IoU over scale 0.79-1.27, rotation +-6 deg and shift +-96 px; this separates a
                *reframed* redraw (low raw, high aligned) from a *reshaped* one (low both)
  scale         the best-fit scale (below 1: the redraw drew the subject larger)

Limits: dark paint on dark space lowers scores; effects crossing the hull cause dips; a shape pass says
nothing about style or texture. Always look at the overlay and the approved art side by side.
Requires numpy, pillow, scipy.
"""
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage


def segment(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722])
    fg = (((b - np.maximum(r, g)) < 0.05) & (luma > 0.07)) | (luma > 0.45)
    fg = ndimage.binary_closing(ndimage.binary_opening(fg, iterations=1), iterations=3)
    return ndimage.binary_fill_holes(fg)


def iou(a, b):
    return float((a & b).sum() / max((a | b).sum(), 1))


def aligned(pred, true, k=4):
    P = np.asarray(Image.fromarray(pred.astype(np.uint8) * 255).resize((pred.shape[1] // k, pred.shape[0] // k))) > 127
    T = np.asarray(Image.fromarray(true.astype(np.uint8) * 255).resize((true.shape[1] // k, true.shape[0] // k))) > 127
    if not P.any() or not T.any():
        return 0.0, 1.0
    ct, cp = np.array(ndimage.center_of_mass(T)), np.array(ndimage.center_of_mass(P))
    best = (iou(P, T), 1.0)
    for s in np.arange(0.79, 1.27, 0.03):
        for a in (-6, -3, 0, 3, 6):
            th = np.deg2rad(a); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]) / s
            for dy in range(-24, 25, 3):
                for dx in range(-24, 25, 3):
                    c0 = cp + np.array([dy, dx])
                    W = ndimage.affine_transform(P.astype(np.float32), R, offset=c0 - R @ ct, order=0) > 0.5
                    v = iou(W, T)
                    if v > best[0]:
                        best = (v, float(s))
    return round(best[0], 3), round(best[1], 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mask"); ap.add_argument("candidates", nargs="+"); ap.add_argument("--overlay-dir")
    a = ap.parse_args()
    true = np.asarray(Image.open(a.mask).convert("L")) > 127
    out = {}
    for c in a.candidates:
        im = Image.open(c).convert("RGB")
        if im.size != (true.shape[1], true.shape[0]):
            im = im.resize((true.shape[1], true.shape[0]), Image.LANCZOS)
        fg = segment(np.asarray(im).astype(np.float32) / 255)
        lab, n = ndimage.label(fg)
        keep = np.isin(lab, [i for i in range(1, n + 1) if (true & (lab == i)).sum() > 0.01 * true.sum()])
        al, sc = aligned(keep, true)
        out[c] = {"raw_iou": round(iou(keep, true), 3), "aligned_iou": al, "scale": sc}
        if a.overlay_dir:
            edge = true & ~ndimage.binary_erosion(true, iterations=2)
            ov = np.asarray(im).copy(); ov[edge] = (0, 255, 255)
            Path(a.overlay_dir).mkdir(parents=True, exist_ok=True)
            Image.fromarray(ov).save(Path(a.overlay_dir) / f"qa-{Path(c).stem}.jpg", quality=88)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
